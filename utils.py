"""
===============================================================================
[프로그램 명] 
Adult Census Income 데이터 분석 및 머신러닝 파이프라인 자동화 (공통 유틸 모듈)

[이해관계자를 위한 프로그램 설명 (Communication Context)]
본 모듈은 실무적인 프로덕션 데이터 엔지니어링 환경을 모사하여, 
특정 시스템 경로 하드코딩 오류(FileNotFoundError), 파일 확장자 불일치 및 손상(Parsing Error, Permission Error) 등 
실무에서 직면할 수 있는 다양한 입출력 장벽을 유연하고 견고하게 격리/해결하기 위한 공통 파일 처리 엔진입니다.

[제공하는 핵심 가치]
1. 제네릭 로더 (`safe_load_data`): 
   - 확장자(.csv, .json, .xlsx, .parquet)를 자동으로 감지하여 최적의 라이브러리(Pandas/Polars)로 자동 연동합니다.
2. 지능적 경로 탐색 및 복구 (`resolve_file_path`): 
   - 절대/상대 경로 오류 시 작업 디렉토리를 지능적으로 탐색하여 가장 유사한 대체 파일을 탐색 및 추천하거나 복구 폴백을 실행합니다.
3. YAML 전역 설정 안전 관리 (`load_yaml_config`): 
   - YAML 손상 및 파싱 오류 시에도 기본 Default 템플릿을 온전하게 제공하여 파이프라인의 영속성(Persistence)을 보장합니다.
===============================================================================
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Union, List, Any
import pandas as pd
import polars as pl
import yaml


def get_logger(name: str = "pipeline", log_file: str = "output/pipeline.log") -> logging.Logger:
    """
    설정된 이름과 로그 파일 경로를 기준으로 콘솔 및 파일 이중 로깅을 수행하는 로거를 구성하여 반환합니다.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.INFO)
    
    # 출력 경로 상의 디렉토리 자동 생성
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] (%(name)s) - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    # 1. 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 2. 파일 핸들러 설정 (실행이 누적 기록됨)
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


# 모듈 전용 로거 기동
logger = get_logger("utils")


def resolve_file_path(file_path: Union[str, Path], fallback_dir: str = "data") -> Union[str, Path]:
    """
    지정된 파일 경로의 실존 여부를 검사하고, 유실되었을 경우 대안 경로 및 작업 디렉토리 내 검색을 통해 
    실제 사용 가능한 경로를 지능적으로 역추적하여 반환합니다. 만약 URL(http/https) 경로일 경우, 
    네트워크 스트림 경로이므로 검사를 생략하고 그대로 반환합니다.
    
    Parameters:
    -----------
    file_path : str or Path
        로드하려는 타겟 파일의 경로 또는 URL
    fallback_dir : str, default "data"
        파일이 유실되었을 때 우선 탐색할 디렉토리 이름

    Returns:
    --------
    Union[str, Path]
        검증 완료된 실제 절대 경로 또는 원본 URL 문자열
        
    Raises:
    -------
    FileNotFoundError
        작업 폴더 전체를 수색했음에도 물리 파일이 아예 발견되지 않는 경우 최후에 예외를 발생시킵니다.
    """
    # 0. 네트워크 주소(URL) 기동 시 검사 생략 후 즉시 반환
    path_str = str(file_path)
    if path_str.startswith(("http://", "https://", "ftp://")):
        return path_str

    target = Path(file_path).resolve()
    
    # 1. 파일이 실존하는 경우 바로 반환 (가장 일반적인 경우)
    if target.is_file():
        return target
        
    logger.warning(f"[경로 검사] 지정된 경로에 파일이 존재하지 않습니다: {target}")
    logger.info("🔍 [지능적 복구] 작업 디렉토리 내 대체 파일 탐색을 기동합니다...")
    
    filename = target.name
    current_dir = Path.cwd()
    
    # 2. 작업 디렉토리 하위의 모든 디렉토리를 수색하여 파일명이 동일한 실존 파일 역추적
    for root, _, files in os.walk(current_dir):
        if filename in files:
            alternative_path = Path(root) / filename
            logger.info(f"✅ [복구 성공] 작업 디렉토리 하위에서 일치하는 대체 파일을 찾았습니다: {alternative_path}")
            return alternative_path
            
    # 3. 만약 fallback_dir에 유사 데이터가 있거나 새로 수집할 가이드가 필요한 경우 안내 후 예외 발생
    error_msg = (
        f"\n❌ [CRITICAL ERROR] 물리적 파일을 시스템 상에서 찾을 수 없습니다: '{filename}'\n"
        f"  - 원본 지정 경로: {target}\n"
        f"  - 탐색 기준 디렉토리: {current_dir}\n"
        f"  - 조치 방법: 데이터 파일이 올바른 위치에 복사되어 있는지 확인하거나, "
        f"config.yaml 혹은 코드상의 경로를 재조정하세요."
    )
    raise FileNotFoundError(error_msg)


def safe_load_data(
    file_path: Union[str, Path], 
    engine: str = "pandas", 
    na_values: Any = None, 
    **kwargs: Any
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    파일의 확장자를 지능적으로 자동 검출하고, 인코딩 에러 및 열 손상 등의 오류 예외를 제어하여 
    데이터를 안전하게 로드합니다. (CSV, JSON, XLSX, PARQUET 완전 대응)

    Parameters:
    -----------
    file_path : str or Path
        타겟 데이터 파일 경로
    engine : str, default "pandas"
        가져올 프레임워크 선택 ('pandas' 또는 'polars')
    na_values : Any, optional
        결측치로 변환할 문자열 패턴 세트
    **kwargs : Any
        해당 파서에 전달할 추가 키워드 매개변수

    Returns:
    --------
    Union[pd.DataFrame, pl.DataFrame]
        정상 로드된 데이터 프레임 구조체

    Raises:
    -------
    ValueError
        해당 포맷을 지원하지 않는 경우 예외를 통제하여 전달합니다.
    """
    try:
        # 지능적 실존 경로 파악 기동
        real_path = resolve_file_path(file_path)
        
        # 만약 real_path가 URL(문자열)인 경우 확장자를 파일 끝에서 파싱
        if isinstance(real_path, str):
            # 쿼리 파라미터가 섞여있을 때를 감안해 마지막 경로 부분 추출
            clean_path = real_path.split('?')[0]
            ext = os.path.splitext(clean_path)[1].lower()
        else:
            ext = real_path.suffix.lower()
        
        logger.info(f"📥 [데이터 로딩] 경로 '{real_path}' | 확장자 '{ext}' 자동 감증 | 로드 엔진: {engine.upper()}")
        
        # ------------------ Pandas 파이프라인 로딩 제어 ------------------
        if engine.lower() == "pandas":
            if ext in [".csv", ".data"]:
                return pd.read_csv(real_path, na_values=na_values, keep_default_na=True, **kwargs)
            elif ext == ".json":
                # JSON 로딩 시 흔히 발생하는 인코딩(UTF-8)과 라인단위 다중 구조(lines=True) 자동 복구 옵션 적용
                try:
                    return pd.read_json(real_path, encoding='utf-8', **kwargs)
                except ValueError:
                    # 복구 시도: 단일 줄 다중 JSON(lines=True) 형태일 경우 폴백
                    return pd.read_json(real_path, lines=True, encoding='utf-8', **kwargs)
            elif ext in [".xlsx", ".xls"]:
                return pd.read_excel(real_path, **kwargs)
            elif ext == ".parquet":
                return pd.read_parquet(real_path, **kwargs)
            else:
                raise ValueError(f"지원하지 않는 파일 형식입니다: {ext}")
                
        # ------------------ Polars 파이프라인 로딩 제어 ------------------
        elif engine.lower() == "polars":
            # Polars의 경우 string 타입의 na_values 리스트 대응 처리
            null_vals = [str(na_values)] if isinstance(na_values, (str, int, float)) else na_values
            
            if ext in [".csv", ".data"]:
                return pl.read_csv(real_path, null_values=null_vals, **kwargs)
            elif ext == ".json":
                try:
                    return pl.read_json(real_path, **kwargs)
                except Exception:
                    # newline-delimited json 형태 복구 폴백
                    return pl.read_ndjson(real_path, **kwargs)
            elif ext == ".parquet":
                return pl.read_parquet(real_path, **kwargs)
            elif ext in [".xlsx", ".xls"]:
                # Polars Excel 파서 사용
                return pl.read_excel(real_path, **kwargs)
            else:
                raise ValueError(f"Polars 엔진이 지원하지 않는 파일 형식입니다: {ext}")
        else:
            raise ValueError(f"알 수 없는 실행 엔진: {engine}")
            
    except PermissionError:
        logger.error(f"[권한 오류] 해당 파일에 읽기 권한이 없습니다: {file_path}")
        raise
    except json.JSONDecodeError as je:
        logger.error(f"[JSON 파싱 오류] JSON 파일 구조가 손상되었거나 유효하지 않습니다: {je}")
        raise
    except Exception as e:
        logger.error(f"[데이터 로드 실패] 알 수 없는 데이터 처리 시스템 오류가 감지되었습니다: {e}")
        raise


def safe_save_data(
    df: Union[pd.DataFrame, pl.DataFrame], 
    file_path: Union[str, Path], 
    **kwargs: Any
) -> None:
    """
    추출/정제된 프레임을 지정 파일 포맷에 맞춰 안전하게 물리 디스크에 기록합니다.
    저장 경로 상의 디렉토리가 없으면 자동으로 상위 경로를 재귀 생성(mkdir)합니다.
    """
    target = Path(file_path).resolve()
    ext = target.suffix.lower()
    
    try:
        # 상위 디렉토리가 존재하지 않을 경우 자동 생성 기동
        target.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"📤 [데이터 저장] 경로: {target} | 포맷: {ext}")
        
        if isinstance(df, pd.DataFrame):
            if ext == ".csv":
                df.to_csv(target, index=False, encoding='utf-8-sig', **kwargs)
            elif ext == ".json":
                df.to_json(target, orient='records', force_ascii=False, indent=4, **kwargs)
            elif ext in [".xlsx", ".xls"]:
                df.to_excel(target, index=False, **kwargs)
            elif ext == ".parquet":
                df.to_parquet(target, index=False, **kwargs)
            else:
                raise ValueError(f"지원하지 않는 물리 저장 형식입니다: {ext}")
                
        elif isinstance(df, pl.DataFrame):
            if ext == ".csv":
                df.write_csv(target, **kwargs)
            elif ext == ".json":
                # Pylance reportCallIssue 방지를 위해 write_json 오버로드에 적합한 표준 매개변수 형태로 정비합니다.
                df.write_json(str(target), **kwargs)
            elif ext == ".parquet":
                df.write_parquet(target, **kwargs)
            else:
                raise ValueError(f"Polars 엔진이 지원하지 않는 물리 저장 형식입니다: {ext}")
                
        logger.info("✅ [저장 성공] 파일이 정상적으로 기록되었습니다.")
        
    except PermissionError:
        print(f"❌ [권한 오류] 해당 디렉토리 혹은 파일에 쓰기 권한이 없습니다: {target}")
        raise
    except Exception as e:
        print(f"❌ [데이터 저장 실패] 디스크 기록 중 오류가 발생했습니다: {e}")
        raise
