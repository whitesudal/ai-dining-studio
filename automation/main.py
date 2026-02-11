import os
import gspread
from google.oauth2.service_account import Credentials

# 1. 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_PATH = os.path.join(BASE_DIR, "service_account.json")

def final_connect():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=scopes)
    client = gspread.authorize(creds)

    # 2. 시트 열기 (이미지 2-3의 ID 사용)
    SHEET_ID = "1JTOOfZTaqImO4aQKEq1itcvggALuy4t5VYipuv4x3xo"
    spreadsheet = client.open_by_key(SHEET_ID)

    # 3. [핵심] 이름과 상관없이 첫 번째 탭(0번)을 무조건 가져오기
    # 이를 통해 '시트 1'이나 'data' 이름 문제를 해결합니다.
    return spreadsheet.get_worksheet(0)

if __name__ == "__main__":
    try:
        ws = final_connect()
        print(f"✅ 드디어 연결 성공! 현재 탭 이름: {ws.title}")
        # 시트의 2행 데이터를 읽어와 출력 (낙지마실 데이터 확인)
        print(f"📊 첫 번째 데이터 행: {ws.row_values(2)}")
    except Exception as e:
        print(f"❌ 연결 실패: {e}")
