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
    """구글 시트 인증을 수행하고 연결된 워크시트 객체를 반환하다."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 서비스 계정 키 파일 경로 설정
    creds_path = os.path.join(BASE_DIR, config["google_credentials"])
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    
    # 시트 열기
    spreadsheet = client.open_by_key(config["google_sheet"]["sheet_id"])
    
    # [진단] 연결 실패 시를 대비해 현재 시트의 모든 탭 이름을 출력하다
    all_tabs = [s.title for s in spreadsheet.worksheets()]
    print(f"🔍 시스템 인식 실제 탭 목록: {all_tabs}")
    
    return spreadsheet.worksheet(config["google_sheet"]["worksheet_name"])

if __name__ == "__main__":
    # 설정 로드
    config = load_config()
    print(f"⚙️ 설정 로드 완료: {config['google_sheet']['worksheet_name']} 연결 시도 중...")

    try:
        # 구글 시트 연결 및 데이터 로드
        ws = authenticate_google_sheets(config)
        print(f"✅ 성공: '{config['google_sheet']['worksheet_name']}' 연결 완료하다.")
        
        # 전체 데이터 읽기
        rows = ws.get_all_records()
        print(f"📊 총 {len(rows
