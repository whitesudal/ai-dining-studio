import os
import yaml
import gspread
from google.oauth2.service_account import Credentials

# 1. 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

def load_config():
    """설정 파일을 로드하여 딕셔너리로 반환하다."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def authenticate_google_sheets(config):
    """구글 시트 인증을 수행하고 워크시트 객체를 반환하다."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 이미지 16번에서 확인한 서비스 계정 파일 경로를 사용하다.
    creds_path = os.path.join(BASE_DIR, config["google_credentials"])
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    
    # 시트 ID와 탭 이름을 사용하여 연결하다.
    spreadsheet = client.open_by_key(config["google_sheet"]["sheet_id"])
    return spreadsheet.worksheet(config["google_sheet"]["worksheet_name"])

if __name__ == "__main__":
    # 설정 로드 및 출력
    config = load_config()
    print(f"CONFIG LOADED: {config}")

    try:
        # 구글 시트 연결 시도
        ws = authenticate_google_sheets(config)
        print(f"✅ 성공: '{config['google_sheet']['worksheet_name']}' 연결 완료하다.")
        
        # 데이터 전체 로드
        data = ws.get_all_records()
        print(f"📊 로드된 데이터 수: {len(data)}행")
        
        # 데이터가 존재할 경우 화면에 출력하다.
        if data:
            print("\n--- 로드된 데이터 상세 ---")
            for i, row in enumerate(data):
                print(f"[{i+1}번 식당]: {row['shop_name']}")
                print(f" - 타겟: {row['audience']}")
                print(f" - 목적: {row['purpose']}")
                print(f" - 점수: Solo({row['solo']}), Family({row['family']}), Tourist({row['tourist']})")

    except Exception as e:
        print(f"❌ 연결 실패 상세 사유: {e}")
        print("팁: 구글 시트 하단 탭 이름이 정확히 '시트 1'인지 확인하다.")
