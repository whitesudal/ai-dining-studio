import os
import gspread
from google.oauth2.service_account import Credentials

# 파일 경로 설정 (이미지 1-10 기준)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_PATH = os.path.join(BASE_DIR, "service_account.json")

def ultimate_connect():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # 1. 인증 정보 로드
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=scopes)
    client = gspread.authorize(creds)

    # 2. 시트 ID로 직접 열기 (이미지 2-3의 sheet_id 사용)
    SHEET_ID = "1JTOOfZTaqImO4aQKEq1itcvggALuy4t5VYipuv4x3xo"
    spreadsheet = client.open_by_key(SHEET_ID)

    # 3. [핵심] 이름과 상관없이 첫 번째 탭(0번)을 무조건 가져오기
    return spreadsheet.get_worksheet(0)

if __name__ == "__main__":
    try:
        print("🚀 구글 시트 직통 연결 시도 중...")
        ws = ultimate_connect()
        print(f"✅ 연결 성공! 현재 접속된 탭 이름: {ws.title}")
        print(f"📄 첫 번째 줄 데이터 확인: {ws.row_values(1)}")
    except Exception as e:
        print(f"❌ 연결 실패 원인: {e}")
