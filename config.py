# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API 키 로드
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("⚠️ Warning: GEMINI_API_KEY environment variable is not set.")

# 챗봇 설정
FILE_STORE_NAME = '챗봇저장소'
DOCS_DIR = "DOCS_DIR"  # 문서가 들어있는 폴더명
MODEL_NAME = "gemini-2.5-flash"

# 재시도 설정
MAX_RETRIES = 3
RETRY_DELAY = 5

# 지도 설정
MAP_IMAGE_PATH = 'map/올공맵.png'
ROADS_GEOJSON_PATH = 'map/roads.geojson'
FACILITIES_JSON_PATH = 'map/olympic_facilities.json'

# 좌표 보정값 설정 (이미지와 좌표가 안 맞을 때 수정)
CALIB_X_OFFSET = 33.0   # 오른쪽(+)이나 왼쪽(-)으로 이동 (픽셀 단위)
CALIB_Y_OFFSET = 33.0   # 아래(+)나 위(-)로 이동
CALIB_X_SCALE = 1.0     # 가로로 늘리기(1.0보다 큼) / 줄이기(1.0보다 작음)
CALIB_Y_SCALE = 1.0     # 세로로 늘리기 / 줄이기
