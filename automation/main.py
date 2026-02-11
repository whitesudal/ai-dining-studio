import os
import yaml
import gspread
from google.oauth2.service_account import Credentials

# 1. 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def authenticate_google_sheets(config):
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # service_account.json이 현재 폴더에 있으므로 경로 수정
    creds_path = os.path.join(os.getcwd(), config["google_credentials"])
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    
    sheet_id = config["google_sheet"]["sheet_id"]
    return client.open_by_key(sheet_id).worksheet(config["google_sheet"]["worksheet_name"])

# --- 실행부 ---
if __name__ == "__main__":
    config = load_config()
    print(f"CONFIG LOADED: {config}")
    
    try:
        # 구글 시트 연결 실행
        ws = authenticate_google_sheets(config)
        print(f"✅ 성공: '{config['google_sheet']['worksheet_name']}' 시트에 연결되었습니다.")
        
        # 전체 데이터 가져오기
        all_data = ws.get_all_records()
        print(f"📊 로드된 데이터 수: {len(all_data)}행")
        
        if all_data:
            print("첫 번째 행 데이터:", all_data[0])
            
    except Exception as e:
        print(f"❌ 연결 실패: {e}")
