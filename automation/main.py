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
    """구글 시트 인증을 수행하고 첫 번째 워크시트 객체를 반환하다."""
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
    
    # [진단] 현재 시트의 모든 탭 이름을 출력하다
    all_tabs = [s.title for s in spreadsheet.worksheets()]
    print(f"🔍 시스템 인식 실제 탭 목록: {all_tabs}")
    
    # 대안 1: 이름 대신 인덱스로 접근 (첫 번째 탭을 강제로 가져오다)
    return spreadsheet.get_worksheet(0)

if __name__ == "__main__":
    # 설정 로드
    config = load_config()
    print(f"⚙️ 설정 로드 완료. 첫 번째 시트 연결 시도 중...")
    
    try:
        worksheet = authenticate_google_sheets(config)
        print(f"✅ 연결 성공: [{worksheet.title}] 탭을 읽어왔습니다.")
        
        # 테스트: A1 셀 내용 출력
        print(f"📄 A1 셀 내용: {worksheet.acell('A1').value}")
        
    except Exception as e:
        print(f"❌ 연결 실패: {e}")
