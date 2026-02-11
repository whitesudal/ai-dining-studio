import os
import yaml
import gspread
from google.oauth2.service_account import Credentials

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def authenticate_google_sheets(config):
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds_path = os.path.join(BASE_DIR, config["google_credentials"])
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    
    sheet_id = config["google_sheet"]["sheet_id"]
    return client.open_by_key(sheet_id).worksheet(config["google_sheet"]["worksheet_name"])

if __name__ == "__main__":
    config = load_config()
    print(f"CONFIG LOADED: {config}")

    try:
        ws = authenticate_google_sheets(config)
        print(f"✅ 성공: '{config['google_sheet']['worksheet_name']}' 연결 완료!")
        
        # 전체 데이터 읽기 및 출력
        rows = ws.get_all_records()
        print(f"📊 총 {len(rows)}개의 데이터를 불러왔습니다.")
        if rows:
            print("데이터 샘플:", rows[0])
            
    except Exception as e:
        print(f"❌ 연결 실패: {e}")
import os
import yaml
import gspread
from google.oauth2.service_account import Credentials

# 1. 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

def load_config():
    """YAML 설정 파일을 로드하여 딕셔너리로 반환하다."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load
