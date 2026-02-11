import os
import yaml

# 1. 경로 설정: 실행 위치에 상관없이 main.py와 같은 폴더의 config.yaml을 찾도록 설정하다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

def load_config():
    """
    YAML 설정 파일을 로드하여 딕셔너리로 반환하다.
    """
    try:
        # 12번 라인 부근: 파일을 읽고 데이터를 반환하도록 수정하다.
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
            
            # 파일이 비어있지 않은지 확인하다.
            if config_data is None:
                print("경고: config.yaml 파일이 비어 있다.")
                return {}
                
            return config_data
            
    except FileNotFoundError:
        print(f"오류: 설정 파일을 찾을 수 없다. 경로: {CONFIG_PATH}")
        return {}
    except yaml.YAMLError as e:
        print(f"오류: YAML 파싱 중 문제가 발생하다: {e}")
        return {}

# 2. 전역 변수 config에 로드된 데이터를 할당하다.
# 이전 코드에서 이 부분이 None을 반환하여 오류가 발생했을 가능성이 크다.
config = load_config()

# 확인을 위한 출력문 (터미널에서 CONFIG LOADED: None이 나오면 안 되다)
print(f"CONFIG LOADED: {config}")

# 26번 라인: 이제 config는 dict 타입이므로 정상적으로 참조 가능하다.
if config and "google_credentials" in config:
    google_credentials = config["google_credentials"]
    # 이후 로직 진행...
else:
    print("오류: config에서 'google_credentials'를 찾을 수 없다.")
