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
            return config_data if config_data else {}
    except FileNotFoundError:
        print(f"오류: 설정 파일을 찾을 수 없다. 경로: {CONFIG_PATH}")
        return {}

def authenticate_google_sheets(config):
    """구글 시트 인증을 수행하고 실제 탭 목록을 출력하다."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets", 
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 인증 파일 경로 설정
    creds_path = os.path.join(BASE_DIR, config["google_credentials"])
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    
    # 시트 열기
    spreadsheet = client.open_by_key(config["google_sheet"]["sheet_id"])
    
    # 🔍 [진단 코드] 현재 시트에 있는 모든 탭 이름을 터미널에 출력하다.
    all_tabs = [s.title for s in spreadsheet.worksheets()]
    print(f"🔍 현재 구글 시트의 실제 탭 목록: {all_tabs}")
    
    # 설정된 이름으로 연결 시도 (현재 '시트 1')
    return spreadsheet.worksheet(config["google_sheet"]["worksheet_name"])

# --- 실행부 ---
if __name__ == "__main__":
    # 1단계: 설정 로드
    config = load_config()
    print(f"CONFIG LOADED: {config}")

    if config:
        try:
            # 2단계: 구글 시트 연결 및 진단
            ws = authenticate_google_sheets(config)
            print(f"✅ 성공: '{config['google_sheet']['worksheet_name']}' 연결 완료하다.")
            
            # 3단계: 데이터 로드 및 출력
            data = ws.get_all_records()
            print(f"📊 로드된 데이터 수: {len(data)}행")
            
            if data:
                print("데이터 샘플 (1행):", data[0])
                
        except
