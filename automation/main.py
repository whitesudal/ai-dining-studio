import os
import yaml
import gspread
from google.oauth2.service_account import Credentials

# 1. 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

def load_config():
    """설정 파일을 읽어오다."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def authenticate_and_get_data(config):
    """구글 시트 인증 및 데이터 추출을 수행하다."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 인증 파일 경로 확인
    creds_path = os.path.join(BASE_DIR, config["google_credentials"])
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    
    # 2단계: 시트 열기
    sheet_id = config["google_sheet"]["sheet_id"]
    spreadsheet = client.open_by_key(sheet_id)
    
    # [디버깅] 현재 시트에 존재하는 모든 탭 이름을 출력하다.
    all_worksheets = [s.title for s in spreadsheet.worksheets()]
    print(f"현재 시트의 실제 탭 목록: {all_worksheets}")
    
    # 3단계: 워크시트 선택
    target_name = config["google_sheet"]["worksheet_name"]
    worksheet = spreadsheet.worksheet(target_name)
    
    # 4단계: 데이터 읽기
    return worksheet.get_all_records()

if __name__ == "__main__":
    config = load_config()
    print(f"CONFIG LOADED: {config}")
    
    try:
        data = authenticate_and_get_data(config)
        print(f"✅ 성공: '{config['google_sheet']['worksheet_name']}' 연결 완료!")
        print(f"📊 총 {len(data)}개의 데이터를 불러오다.")
        
        if data:
            print("데이터 샘플 (1행):", data[0])
            
    except gspread.exceptions.WorksheetNotFound:
        print(f"❌ 오류: '{config['google_sheet']['worksheet_name']}' 탭을 찾을 수 없다. 위 목록 중 하나로 이름을 수정하다.")
    except Exception as e:
        print(f"❌ 연결 실패 상세 사유: {e}")
