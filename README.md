# 📊 Adult Census Income 데이터 분석 및 머신러닝 파이프라인 자동화

SKALA 광주 캠퍼스 4반 2조의 종합 과제 데이터 파이프라인 프로젝트입니다.  
본 프로젝트는 **UCI Adult Census Income** 데이터셋을 바탕으로 데이터 수집(ETL), 분석(EDA), 가설 검정(T-test), 정적/동적 시각화, Scikit-learn Pipeline 기반 머신러닝 모델 학습/평가 및 결과 보고서 자동 생성까지의 전 과정을 자동화한 엔드투엔드(End-to-End) MLOps 지향형 애플리케이션입니다.

---

## 🛠️ 기술 스택 및 환경
* **언어:** Python `3.11.15`
* **가상환경:** `venv`
* **주요 패키지:**
  * **ETL & EDA:** `pandas`, `polars` (성능 비교 분석용)
  * **통계 분석:** `scipy` (Welch's t-test), `numpy`
  * **시각화:** `matplotlib`, `seaborn` (정적), `plotly` (동적/인터랙티브)
  * **머신러닝:** `scikit-learn` (Pipeline, ColumnTransformer, RandomForest)
  * **모델 관리:** `joblib` (파이프라인 모델 직렬화)
  * **설정 관리:** `PyYAML` (설정 및 모델 파라미터 제어)

---

## 📂 프로젝트 구조
```text
skala-gwangju-4class-team2/
│
├── config.yaml          # 파일 경로, 특성 이름 및 하이퍼파라미터 정의 설정 파일
├── utils.py             # 실무 지향형 파일 처리 엔진 (자동 경로 추적, 스마트 포맷 파서, 예외 처리 격리)
├── data_prep.py         # 공통 유틸리티(폰트), ETL, 가설 검정(T-test) 및 EDA 전담 모듈
├── main.py              # 전체 파이프라인 실행, 시각화, ML 학습/평가 및 마크다운 리포팅 전담 메인 모듈
├── requirements.txt     # 프로젝트 구동에 필요한 라이브러리 목록 파일
│
├── output/              # 파이프라인 실행 결과물 자동 생성 디렉토리
│   ├── adult_income_pipeline.joblib   # 전처리+모델이 통합된 MLOps 서빙 규격 파일
│   ├── plotly_income_distribution.html # 소득 수준별 연령 분포 인터랙티브 차트
│   ├── seaborn_static_charts.png       # 고해상도(300 DPI) 상관관계 및 분포 정적 차트
│   └── report.md                       # 분석 및 평과 결과를 집약한 마크다운 분석 리포트
│
└── README.md            # 과제 가이드 및 프로젝트 상세 매뉴얼 (본 파일)
```

---

## 🚀 파이프라인 가동 및 실행 방법

### 1. 가상환경 활성화 및 패키지 설치
터미널을 열고 본 프로젝트 폴더로 이동한 뒤 가상환경을 활성화하고 패키지를 설치합니다:

```bash
# 가상환경 활성화
source venv/bin/activate

# 의존성 패키지 설치
pip install -r requirements.txt
```

### 2. 전체 파이프라인 실행
설정이 완료되었으면 다음 명령어로 전 과정을 자동으로 구동시킵니다:

```bash
python main.py
```

### 3. 산출물 확인
실행이 완료되면 자동으로 브라우저에 Plotly 인터랙티브 차트가 열리며, `output/` 디렉토리에 다음 결과물이 저장됩니다:
* `output/seaborn_static_charts.png`: 정적 시각화 이미지
* `output/plotly_income_distribution.html`: 동적 시각화 차트
* `output/adult_income_pipeline.joblib`: 학습 완료된 머신러닝 파이프라인 모델
* `output/report.md`: 자동 작성된 데이터 분석 종합 요약 보고서

---

## 📊 종합 과제 체크리스트 완수 현황

| 평가 항목 | 세부 필수 요건 | 구현 상태 | 관련 함수 / 설명 |
| :--- | :--- | :---: | :--- |
| **데이터 준비** | Pandas 데이터 로드 및 Polars 동일 데이터 로드 속도 벤치마킹 | **완료** | `data_prep.py` -> `load_and_clean_data` |
| | 결측치(NaN/?) 유실값 검사 및 정제 처리 | **완료** | `load_and_clean_data` (4,262개 누락 행 제거) |
| | 중복값 검사 및 완벽 소거 (`drop_duplicates`) | **완료** | `load_and_clean_data` (중복 23개 소거) |
| | 기본 EDA 수행 및 콘솔 데이터 출력 (`describe`, `value_counts`) | **완료** | 수치/범주형 분류, `describe()`, 타겟 `value_counts()` 구현 완료 |
| **통계 분석** | 수치형 변수 간 Pearson 상관계수 행렬 구하기 | **완료** | `data_prep.py` -> `perform_eda_and_stats` (fnlwgt 가중치 배제) |
| | 성별 주당 근무시간 평균 차이 t-test (`scipy.stats.ttest_ind`) | **완료** | `perform_eda_and_stats` (이분산성 가정 Welch's t-test 적용) |
| | p-value 가설 해석 도출 | **완료** | $p \approx 0.000$ ➔ 성별 간 근무시간 평균 차이 통계적 검정 완료 |
| **시각화** | Seaborn 정적 차트 1개 이상 (히트맵, 박스플롯) | **완료** | `main.py` -> `generate_visualizations` (2개 서브플롯 병합) |
| | Plotly 인터랙티브 차트 1개 이상 (히스토그램 오버레이) | **완료** | `generate_visualizations` (마우스 오버/줌인 기능 포함) |
| | 차트 제목, X축 레이블, Y축 레이블 한글 필수 기입 | **완료** | OS별 감지 한글 폰트 적용 및 축 이름 명시 지정 |
| **머신러닝** | `sklearn.pipeline.Pipeline` 객체 기반 통합 | **완료** | `main.py` -> `build_and_evaluate_pipeline` |
| | 결측 대치 및 스케일러/인코더와 RandomForest 결합 | **완료** | `ColumnTransformer` (Imputer, Scaler, OneHot) + `Classifier` |
| | 평가 지표 다각도 출력 (Accuracy, F1, Precision, Recall, Confusion Matrix) | **완료** | 정확도 84.37%, F1 0.6778 및 정밀 평가지표 출력 완수 |
| | `joblib.dump()` 활용 모델 이진 파일 직렬화 관리 | **완료** | `adult_income_pipeline.joblib` 저장 (MLOps 서빙 규격 충족) |
| **자동화** | 실행 시 마크다운 종합 리포트 자동 생성 (`report.md`) | **완료** | `main.py` -> `generate_automated_report` |
| **코드 품질** | 가독성 우수 및 함수/모듈 설계, 풍부한 한글 주석 | **완료** | 주석 50% 이상, `data_prep` 유틸 분리 및 `config.yaml` 연동 완수 |
| | 실무형 공통 I/O 처리 모듈 분리 및 예외 핸들링 강화 | **완료** | `utils.py` 내 지능형 경로 역추적 및 통합 파서 구축 완수 |

---

## 📝 데이터 분석 및 모델링 결과 해석 요약

### 1. Pandas vs Polars 로딩 비교 분석
* **Pandas:** 단일 스레드로 메모리에 즉시 Eager 파싱을 수행하여 편리하고 정형화된 데이터 탐색(`describe()`, `dtypes`)이 가능합니다.
* **Polars:** Rust 기반 다중 스레드 병렬 로딩 및 벡터화(SIMD) 가속화로 대용량 데이터에서 압도적으로 우수한 로딩 시간 단축 효과를 보입니다.

### 2. t-test 가설 검정 해석
* **t-statistic:** `41.665` | **p-value:** `0.000e+00`
* **해석:** 유의수준 5%($\alpha = 0.05$) 하에서 p-value가 매우 작으므로, 남성과 여성의 주당 근무시간 평균에 차이가 없다는 귀무가설($H_0$)을 확실히 기각합니다. 즉, 남성 노동 집단의 평균 근무시간이 통계적으로 유의미하게 깁니다.

### 3. 예측 모델 성능 분석
* **선택 모델:** RandomForest (결정 나무 앙상블 기법)
* **Accuracy:** `84.37%`
* **F1-Score:** `0.6778` (Precision: `0.7176`, Recall: `0.6423`)
* **인사이트:** 모델의 정확도가 매우 뛰어나며, 전처리와 모델을 Pipeline으로 병합 관리하여 새로운 고객 데이터가 실시간 API 등으로 연동되더라도 데이터 누수(Leakage)나 차원 크기 오류(Dimension mismatch) 없이 안전하고 동일하게 연소득 이진 예측을 추론해 낼 수 있는 프로덕션 가치를 확보했습니다.

---

## 💎 추가 제언 및 아키텍처 개선 방향
1. **결측치 대치 고도화:** 현재 행 삭제(`dropna()`) 처리를 진행했으나, 데이터 소실을 막기 위해 Pandas/Polars 단계에서 최빈값이나 예측 기반 대치(예: KNNImputer)를 도입할 수 있습니다.
2. **클래스 불균형 완화:** 연소득 50K 이하가 약 75%를 점유하고 있으므로, 오버샘플링(SMOTE) 기술을 Pipeline 단계에 통합(`imblearn.pipeline`)하면 F1-Score를 극대화할 수 있습니다.
3. **하이퍼파라미터 최적화:** `GridSearchCV` 또는 `RandomizedSearchCV`를 전처리 파이프라인에 중첩 연결하여 데이터 스케일 변경에 따른 랜덤포레스트 모델의 트레이드 오프 관계를 완전 자동 튜닝하도록 확장 가능합니다.
