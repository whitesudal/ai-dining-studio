import os
import gspread
from google.oauth2.service_account import Credentials

# 파일 경로 설정 (이미지 1-10 기준)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_PATH = os.path.join(BASE_DIR, "service_account.json")

def final_connect():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=scopes)
    client = gspread.authorize(creds)

    # 시트 ID로 직접 접속
    SHEET_ID = "1JTOOfZTaqImO4aQKEq1itcvggALuy4t5VYipuv4x3xo"
    spreadsheet = client.open_by_key(SHEET_ID)

    # [핵심] 이름과 상관없이 첫 번째 탭(0번)을 무조건 가져옴
    return spreadsheet.get_worksheet(0)

if __name__ == "__main__":
    try:
        ws = final_connect()
        print(f"✅ 드디어 연결 성공! 탭 이름: {ws.title}")
        print(f"📊 첫 번째 줄 데이터: {ws.row_values(1)}")
    except Exception as e:
        print(f"❌ 아직 연결 실패: {e}")
