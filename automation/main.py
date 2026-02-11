import os
import yaml

# 1. 경로 설정 (main.py와 config.yaml이 같은 폴더에 있을 때)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

# 2. 설정 로드 함수 정의
def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data  # 로드된 데이터를 반환함
    except FileNotFoundError:
        print(f"설정 파일을 찾을 수 없습니다: {CONFIG_PATH}")
        return None

# 3. 변수에 할당 (이 부분이 핵심입니다!)
config = load_config()

# 확인용 출력
print(f"CONFIG LOADED: {config}")

# 이제 26번 라인 근처의 코드가 정상 작동할 것입니다.
if config:
    credentials = config["google_credentials"]
    # ... 나머지 코드 ...
