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
    # 권한 범위 설정
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds_path = os.path.join(BASE_DIR, config["google_credentials"])
    
    # 인증 수행
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    
    # 시트 열기
    sheet_id = config["google_sheet"]["sheet_id"]
    spreadsheet = client.open_by_key(sheet_id)
    
    # 특정 워크시트 선택 (여기서 실패할 경우 상세 메시지 출력)
    return spreadsheet.worksheet(config["google_sheet"]["worksheet_name"])

if __name__ == "__main__":
    config = load_config()
    print(f"CONFIG LOADED: {config}")

    try:
        # 1. 시트 연결 시도
        ws = authenticate_google_sheets(config)
        print(f"✅ 성공: '{config['google_sheet']['worksheet_name']}' 연결 완료!")
        
        # 2. 데이터 읽기 (전체 레코드를 리스트로 가져옴)
        rows = ws.get_all_records()
        print(f"📊 총 {len(rows)}개의 데이터를 불러왔습니다.")
        
        # 3. 데이터 출력 (첫 5행만 예시로 출력)
        if rows:
            print("\n--- 데이터 샘플 ---")
            for row in rows[:5]:
                print(row)
                
    except gspread.exceptions.WorksheetNotFound:
        print(f"❌ 오류: '{config['google_sheet']['worksheet_name']}'라는 이름의 시트 탭을 찾을 수 없습니다.")
    except Exception as e:
        print(f"❌ 연결 실패 상세 사유: {e}")
