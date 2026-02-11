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
    
    spreadsheet = client.open_by_key(config["google_sheet"]["sheet_id"])
    
    # 🔍 [핵심 디버깅] 현재 시트에 존재하는 모든 탭 이름을 강제로 출력합니다.
    all_tabs = [s.title for s in spreadsheet.worksheets()]
    print(f"🔍 시스템이 인식한 실제 탭 목록: {all_tabs}")
    
    return spreadsheet.worksheet(config["google_sheet"]["worksheet_name"])

if __name__ == "__main__":
    config = load_config()
    try:
        ws = authenticate_google_sheets(config)
        print(f"✅ 성공: '{config['google_sheet']['worksheet_name']}' 연결 완료!")
        
        data = ws.get_all_records()
        print(f"📊 총 {len(data)}행의 데이터를 불러왔습니다.")
        if data:
            print("첫 번째 행 샘플:", data[0])
            
    except Exception as e:
        print(f"❌ 연결 실패: {e}")
