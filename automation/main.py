import os
import gspread
from google.oauth2.service_account import Credentials

# 1. 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_PATH = os.path.join(BASE_DIR, "service_account.json")

def direct_connect():
    """이름 설정을 무시하고 URL로 직접 첫 번째 시트에 연결한다."""
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # 인증 파일 존재 여부 확인
    if not os.path.exists(CREDS_PATH):
        print(f"❌ 파일을 찾을 수 없습니다: {CREDS_PATH}")
        return None

    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=scopes)
    client = gspread.authorize(creds)

    # 2. 시트 URL로 직접 열기 (ID 오타 방지)
    sheet_url = "https://docs.google.com/spreadsheets/d/1JTOOfZTaqImO4aQKEq1itcvggALuy4t5VYipuv4x3xo/edit"
    spreadsheet = client.open_by_url(sheet_url)

    # 3. 이름과 상관없이 첫 번째 탭(0번)을 무조건 가져오기
    return spreadsheet.get_worksheet(0)

if __name__ == "__main__":
    try:
        print("🚀 구글 시트 직통 연결 시도 중...")
        ws = direct_connect()
        if ws:
            print(f"✅ 연결 성공! 현재 접속된 탭 이름: {ws.title}")
            print(f"📄 첫 번째 줄 데이터 확인: {ws.row_values(1)}")
    except Exception as e:
        print(f"❌ 최종 연결 실패 원인: {e}")
