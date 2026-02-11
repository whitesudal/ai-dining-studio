import os
import yaml
import gspread
from google.oauth2.service_account import Credentials

# 1. 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

def load_config():
    """설정 파일을 로드하여 딕셔너리로 반환합니다."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def authenticate_google_sheets(config):
    """구글 시트 인증을 수행하고 시트 객체를 반환합니다."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 서비스 계정 키 파일 경로 설정
    creds_path = os.path.join(BASE_DIR, config["google_credentials"])
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    
    # 시트 열기 (config에 설정된 sheet_id 사용)
    spreadsheet = client.open_by_key(config["google_sheet"]["sheet_id"])
    
    # [진단] 현재 시트의 모든 탭 이름을 출력합니다.
    all_tabs = [s.title for s in spreadsheet.worksheets()]
    print(f"🔍 시스템 인식 실제 탭 목록: {all_tabs}")
    
    # 대안 적용: 이름 대신 인덱스(0)를 사용하여 첫 번째 탭을 강제로 가져옵니다.
    # 이 방식은 'data'나 '시트 1' 같은 이름 오류를 완전히 무시합니다.
    return spreadsheet.get_worksheet(0)

if __name__ == "__main__":
    try:
        # 설정 로드
        config = load_config()
        print(f"⚙️ 설정 로드 완료. 시트 연결 시도 중...")
        
        # 시트 연결
        worksheet = authenticate_google_sheets(config)
        print(f"✅ 연결 성공: [{worksheet.title}] 탭에 접속했습니다.")
        
        # 데이터 확인 (A1 셀 내용 출력)
        sample_data = worksheet.acell('A1').value
        print(f"📄 데이터 샘플 (A1): {sample_data}")
        
    except Exception as e:
        print(f"❌ 최종 연결 실패: {e}")
        print("💡 팁: 구글 시트 우측 상단 '공유' 버튼을 눌러 서비스 계정 이메일이 추가되었는지 다시 확인하세요.")
