import os
import yaml
import gspread
from google.oauth2.service_account import Credentials

# 1. 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

def load_config():
    """YAML 설정 파일을 로드하다."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
            if config_data is None:
                return {}
            return config_data
    except FileNotFoundError:
        print(f"오류: 설정 파일을 찾을 수 없다. 경로: {CONFIG_PATH}")
        return {}

def authenticate_google_sheets(config):
    """구글 시트 API 인증 및 연결을 수행하다."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    try:
        # service_account.json 파일 경로 설정
        creds_path = os.path.join(BASE_DIR, config["google_credentials"])
        
        # 인증 및 클라이언트 생성
        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        client = gspread.authorize(creds)
        
        # 시트 열기
        sheet_id = config["google_sheet"]["sheet_id"]
        spreadsheet = client.open_by_key(sheet_id)
        
        # 워크시트 선택
        worksheet_name = config["google_sheet"]["worksheet_name"]
        worksheet = spreadsheet.worksheet(worksheet_name)
        
        return worksheet
    except Exception as e:
        print(f"구글 시트 연결 중 오류 발생: {e}")
        return None

# --- 실행부 ---
if __name__ == "__main__":
    # 1단계: 설정 로드 (기존 오류 해결 지점)
    config = load_config()
    print(f"CONFIG LOADED: {config}")

    if config and "google_credentials" in config:
        # 2단계: 구글 시트 연결
        ws = authenticate_google_sheets(config)
        
        if ws:
            print(f"성공: '{config['google_sheet']['worksheet_name']}' 시트에 연결되다.")
            
            # 3단계: 데이터 확인 (첫 번째 행 읽기)
            try:
                data = ws.get_all_records()
                print(f"데이터 로드 성공: 총 {len(data)}개의 행을 불러오다.")
                if data:
                    print("첫 번째 데이터 샘플:", data[0])
            except Exception as e:
                print(f"데이터 읽기 오류: {e}")
    else:
        print("오류: 설정을 불러오지 못했거나 인증 정보가 없다.")
