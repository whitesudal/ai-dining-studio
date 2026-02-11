import os
import gspread
from google.oauth2.service_account import Credentials

# 파일 경로 설정 (이미지 1-10 기준)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_PATH = os.path.join(BASE_DIR, "service_account.json")

def direct_connect():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=scopes)
    client = gspread.authorize(creds)

    # 이미지 2-3에 적힌 시트 ID 직접 입력 (오타 방지)
    SHEET_ID = "1JTOOfZTaqImO4aQKEq1itcvggALuy4t5VYipuv4x3xo"
    spreadsheet = client.open_by_key(SHEET_ID)

    # [핵심] 이름 설정을 완전히 무시하고 첫 번째 탭(0번)을 가져옴
    return spreadsheet.get_worksheet(0)

if __name__ == "__main__":
    try:
        print("🚀 구글 시트 직통 연결 시도 중...")
        ws = direct_connect()
        print(f"✅ 연결 성공! 현재 탭 이름: {ws.title}")
        print(f"📄 첫 번째 줄 데이터 확인: {ws.row_values(1)}")
    except Exception as e:
        print(f"❌ 최종 연결 실패 원인: {e}")

