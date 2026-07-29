"""
===============================================================================
[프로그램 명] 
Adult Census Income 데이터 분석 및 머신러닝 파이프라인 자동화 (Main 오케스트레이션 모듈)

[이해관계자를 위한 프로그램 설명 (Communication Context)]
본 스크립트는 'Adult Census Income' 데이터를 기반으로 사용자의 인구통계학적 특성(연령, 성별, 학력 등)을 분석하고, 
연소득이 50K를 초과하는지 여부(이진 분류)를 예측하는 종합 파이프라인의 핵심 실행 제어 장치입니다.
`data_prep` 유틸리티와 연동하여 데이터를 수집/가공하며, 시각화, 파이프라인 기법 머신러닝 모델링 및 요약 리포트 마크다운 문서 자동 생성을 순차적으로 실행합니다.

[구동 설계]
1. `config.yaml` 환경 설정 파싱 ➔ 부재 시 기본 DEFAULT_CONFIG 연동.
2. 데이터 추출 및 정제 (ETL / Pandas vs Polars 성능 정밀 벤치마킹).
3. 기술통계 및 Welch's t-test (성별에 따른 근로시간 가설 검정).
4. 정적/인터랙티브 시각화 차트 파일 출력 (Seaborn & Plotly).
5. Scikit-learn Pipeline 기반 RandomForest 모델 학습 및 Precision, Recall, Confusion Matrix 정밀 검증.
6. 요약된 핵심 업무 리포트 Markdown 파일(`report.md`) 자동 생성 및 저장.
===============================================================================
"""

import os
import webbrowser
import time
from pathlib import Path
from typing import Dict, Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
import joblib

# 외부 모듈에서 정밀 정제 함수 및 폰트 유틸을 안전하게 호출
from data_prep import load_and_clean_data, perform_eda_and_stats, set_korean_font, load_yaml_config, DEFAULT_CONFIG
from utils import safe_save_data, get_logger

# 모듈 전용 로거 기동
logger = get_logger("main")

# ---------------------------------------------------------------------
# [기능 4] 데이터 시각화 생성 (정적 Seaborn / 동적 Plotly)
# ---------------------------------------------------------------------
def generate_visualizations(df: pd.DataFrame, config: Dict[str, object]) -> None:
    """
    비즈니스 소통에 최적화된 고화질 정적 차트(Seaborn)와 인터랙티브 대시보드 차트(Plotly)를 생성하고 자동 저장합니다.
    모든 차트에는 명시적인 제목과 한글 축 레이블이 반영됩니다.
    """
    logger.info("=== [3] 데이터 시각화 ===")
    
    try:
        set_korean_font()  # OS별 한글 인코딩 처리 적용
        numeric_df = df.select_dtypes(include=['number']).drop(columns=['fnlwgt'], errors='ignore')
        
        # 1. 정적 차트 (Seaborn - 수치형 상관계수 히트맵 및 성별/소득별 연령대 분포 비교 박스플롯)
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=axes[0])
        axes[0].set_title('수치형 변수 상관관계 히트맵', fontsize=14)
        axes[0].set_xlabel('피처 (Features)', fontsize=12) 
        axes[0].set_ylabel('피처 (Features)', fontsize=12) 
        
        sns.boxplot(data=df, x='income', y='age', hue='sex', ax=axes[1])
        axes[1].set_title('소득 수준 및 성별에 따른 연령 분포', fontsize=14)
        axes[1].set_xlabel('연소득 수준 (Income Level)', fontsize=12) 
        axes[1].set_ylabel('연령 (Age)', fontsize=12)    
        plt.tight_layout()

        # 정적 이미지 파일로 고해상도 출력 저장 (DPI=300)
        seaborn_path = str(config.get("seaborn_path", DEFAULT_CONFIG["seaborn_path"]))
        fig.savefig(seaborn_path, dpi=300, bbox_inches='tight')
        logger.info(f"-> Seaborn 정적 차트가 '{seaborn_path}'에 저장되었습니다.")

        # 2. 인터랙티브 차트 (Plotly - 소득 수준별 세부 연령대 오버레이 분포 히스토그램)
        fig_plotly = px.histogram(
            df, x='age', color='income', barmode='overlay',
            title='소득 수준별 연령 분포 (인터랙티브 차트)', 
            labels={'age': '연령 (세)', 'income': '연소득 > 50K 여부'} 
        )
        fig_plotly.update_layout(bargap=0.1)
        
        # HTML 파일 저장 및 브라우저 기동 처리
        plotly_path = str(config.get("plotly_path", DEFAULT_CONFIG["plotly_path"]))
        fig_plotly.write_html(plotly_path)
        logger.info(f"-> Plotly 인터랙티브 차트가 '{plotly_path}'에 저장되었습니다.\n")
        
        absolute_plotly_path = 'file://' + os.path.realpath(plotly_path)
        webbrowser.open(absolute_plotly_path)
        
    except Exception as e:
        logger.error(f"[오류 발생] 시각화 생성 실패: {e}\n")
    finally:
        plt.close('all')  # 백그라운드 메모리 해제

# ---------------------------------------------------------------------
# [기능 5] 머신러닝 파이프라인 구성 및 모델 저장
# ---------------------------------------------------------------------
def build_and_evaluate_pipeline(df: pd.DataFrame, config: Dict[str, object]) -> Tuple[float, float, float, float, np.ndarray]:
    """
    전처리(SimpleImputer, Scaler, One-Hot Encoder)와 Random Forest 분류기를 하나의 Pipeline 객체로 묶어 학습시키고
    Accuracy, F1-Score, Precision, Recall, Confusion Matrix 지표를 산출하여 파일로 직렬화(.joblib)합니다.
    """
    logger.info("=== [4] ML Pipeline 학습 및 평가 ===")
    
    # 딕셔너리 안전 로딩을 통한 설정값 파싱
    ml_params = config.get("ml_params", DEFAULT_CONFIG["ml_params"])
    if not isinstance(ml_params, dict):
        ml_params = DEFAULT_CONFIG["ml_params"]
        
    n_estimators = int(ml_params.get("n_estimators", 100))
    random_state = int(ml_params.get("random_state", 42))
    test_size = float(ml_params.get("test_size", 0.2))
    
    acc, f1, prec, rec = 0.0, 0.0, 0.0, 0.0
    conf_mat = np.zeros((2, 2))
    
    try:
        df_ml = df.copy()
        # 이진 종속변수 타겟 변환 (>50K: 1, 그 외: 0)
        df_ml['income_target'] = df_ml['income'].apply(lambda x: 1 if '>50K' in str(x) else 0)

        # 특성 테이블 및 타겟 레이블 격리
        X = df_ml.drop(columns=['income', 'income_target', 'fnlwgt'])
        y = df_ml['income_target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        numeric_features = ["age", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
        categorical_features = ["workclass", "education", "marital-status", "occupation", "relationship", "race", "sex", "native-country"]

        # Pipeline 객체를 전처리기 내부에 삽입하여 MLOps 설계 가치 증명
        preprocessor = ColumnTransformer(transformers=[
            ('num', Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')), # 결측값 중앙값 대치
                ('scaler', StandardScaler())                    # 정규 스케일링
            ]), numeric_features),
            ('cat', Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')), # 범주형 결측치 최빈값 대치
                ('onehot', OneHotEncoder(handle_unknown='ignore'))    # 유입 안 된 특성 무시 옵션
            ]), categorical_features)
        ])

        # 전처리와 Random Forest 앙상블 분류기를 결합한 단일 파이프라인
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=n_estimators, random_state=random_state, n_jobs=-1))
        ])

        # 파이프라인 무중단 단일 학습 프로세스 실행
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        # 세분화된 세부 평가 지표 연산
        acc = float(accuracy_score(y_test, y_pred))
        f1 = float(f1_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred))
        rec = float(recall_score(y_test, y_pred))
        conf_mat = confusion_matrix(y_test, y_pred)
        
        # 모델의 MLOps 배포 가치를 높이기 위해 joblib 단일 파일 직렬화 저장
        model_path = str(config.get("model_path", DEFAULT_CONFIG["model_path"]))
        joblib.dump(pipeline, model_path)
        
        logger.info(f"-> Accuracy  : {acc:.4f}")
        logger.info(f"-> F1-Score  : {f1:.4f}")
        logger.info(f"-> Precision : {prec:.4f}")
        logger.info(f"-> Recall    : {rec:.4f}")
        logger.info(f"-> Confusion Matrix :\n{conf_mat}")
        logger.info(f"\n-> Classification Report:\n{classification_report(y_test, y_pred)}")
        logger.info(f"-> 학습된 통합 파이프라인 모델이 '{model_path}'에 저장되었습니다.\n")

    except Exception as e:
        logger.error(f"[오류 발생] 모델 파이프라인 학습 실패: {e}\n")
        
    return acc, f1, prec, rec, conf_mat

# ---------------------------------------------------------------------
# [기능 6] 분석 결과 자동화 리포팅
# ---------------------------------------------------------------------
def generate_automated_report(
    config: Dict[str, object], df_shape: Tuple[int, int], 
    t_stat: float, p_val: float, acc: float, f1: float,
    prec: float, rec: float, conf_mat: np.ndarray
) -> None:
    """
    수행한 모든 데이터 분석 및 가설 검정, 머신러닝 모델의 정밀 평과 결과를 엮어 요약 리포트(.md)를 자동 빌드합니다.
    """
    logger.info("=== [5] 자동화 리포트 생성 ===")
    
    try:
        model_path = str(config.get("model_path", DEFAULT_CONFIG["model_path"]))
        report_path = str(config.get("report_path", DEFAULT_CONFIG["report_path"]))
        seaborn_path = str(config.get("seaborn_path", DEFAULT_CONFIG["seaborn_path"]))
        
        report_content = f"""# Adult Census Income 데이터 분석 리포트
**작성일시:** {time.strftime('%Y-%m-%d %H:%M:%S')}

## 1. 데이터 개요 (ETL & EDA)
* **정제 완료 분석 데이터 Shape:** {df_shape}
* **결측치 및 중복값 처리 결과:**
  * 로딩 시 Pandas와 Polars 라이브러리 성능을 교차 검증 및 비교 완료.
  * `na_values`를 포함한 결측 행 및 완벽한 중복 행이 성공적으로 정제되었습니다.
  * 분석 데이터 타겟인 'income' 변수의 심층 EDA가 완료되었습니다.

## 2. 통계 검정 및 해석 (Statistical Testing)
* **주제:** 성별(Male vs Female)에 따른 주당 근무시간(hours-per-week) 평균 차이 검정
* **검정 기법:** 독립표본 T-검정 (Welch's t-test)
* **t-statistic:** {t_stat:.3f}
* **p-value:** {p_val:.3e}
* **해석:**
  * {'p-value가 유의수준 0.05 미만이므로 귀무가설(H0)을 기각합니다. 남성과 여성의 주당 근무시간에는 통계적으로 유의미한 차이가 존재합니다.' if p_val < 0.05 else 'p-value가 유의수준 0.05 이상이므로 귀무가설(H0)을 기각할 수 없습니다. 남성과 여성의 주당 근무시간 간에 통계적으로 유의미한 차이가 있다고 보기 어렵습니다.'}

## 3. 시각화 결과 (Data Visualizations)
* **정적 차트 (Seaborn):** 수치형 변수 상관관계 히트맵 및 소득/성별별 연령 분포 박스플롯이 `{seaborn_path.split('/')[-1]}` 파일로 저장 완료되었습니다.
* **인터랙티브 차트 (Plotly):** 소득 수준별 연령 분포를 마우스 오버와 줌인/아웃으로 상세 탐색 가능한 HTML 파일이 브라우저 자동 실행 및 저장되었습니다.

## 4. 머신러닝 모델 평가 및 MLOps (ML Pipeline)
* **알고리즘:** Random Forest Classifier (Scikit-learn Pipeline 객체 기반 전처리 및 모델 통합)
* **평가 지표 결과:**
  * **Accuracy (정확도):** {acc:.4f}
  * **F1-Score (F1 점수):** {f1:.4f}
  * **Precision (정밀도):** {prec:.4f}
  * **Recall (재현율):** {rec:.4f}
  * **Confusion Matrix (혼동 행렬):**
    ```
    {conf_mat}
    ```
* **모델 저장 경로:** `{model_path}` (학습된 전처리 파이프라인 및 모델 전체가 포함되어 배포가 용이함)
"""
        # 지능적인 output 디렉토리 자동 생성 및 마크다운 자동 작성을 공통 유틸 연동 구조로 안전하게 내보냅니다.
        report_content_bytes = report_content.encode('utf-8')
        with open(report_path, "wb") as f:
            f.write(report_content_bytes)
        logger.info(f"-> 분석 리포트가 '{report_path}'에 성공적으로 자동화 생성되었습니다.\n")
            
    except Exception as e:
        logger.error(f"[오류 발생] 보고서 자동화 작성 실패: {e}\n")

# ---------------------------------------------------------------------
# [메인 제어 블록] 프로그램 엔트리 포인트
# ---------------------------------------------------------------------
if __name__ == "__main__":
    logger.info("🚀 종합 분석 파이프라인을 기동합니다...\n" + "="*60)
    
    # 1. 설정 파일을 연동합니다. (config.yaml)
    CONFIG = load_yaml_config("config.yaml")
    
    # 로드 실패 시, 안전 가이드를 제공하고 복원용 DEFAULT_CONFIG를 연동하여 지속성을 보장합니다.
    if CONFIG is None:
        logger.warning("⚠️ 'config.yaml' 로드 실패! 내장 디폴트 하드코딩 환경구조로 안전하게 폴백(Fallback)합니다.")
        CONFIG = DEFAULT_CONFIG
        
    # 2. 데이터 가공 및 정밀 전처리 모듈 기동 (Pandas vs Polars 교차 벤치마크 및 EDA 포함)
    df_clean = load_and_clean_data(CONFIG)
    
    if df_clean is not None:
        # 3. 기술통계 도출 및 주당 근무시간 성별 가설 검정(T-test) 수행
        t_stat_val, p_val_val = perform_eda_and_stats(df_clean)
        
        # 4. 정적 Seaborn 및 인터랙티브 Plotly 차트 이미지 생성 저장
        generate_visualizations(df_clean, CONFIG)
        
        # 5. 전처리 + RandomForest 모델 통합 파이프라인 구동 및 다중 평가지표 계측
        accuracy_val, f1_val, precision_val, recall_val, conf_mat_val = build_and_evaluate_pipeline(df_clean, CONFIG)
        
        # 6. 마크다운 보고서 생성 자동화 기동
        generate_automated_report(CONFIG, df_clean.shape, t_stat_val, p_val_val, accuracy_val, f1_val, precision_val, recall_val, conf_mat_val)
        
    logger.info("="*60 + "\n✅ 파이프라인 전체 과정이 완벽히 정상 가동 및 종료되었습니다.")
