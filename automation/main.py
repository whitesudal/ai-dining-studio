import os
import yaml
import gspread
from google.oauth2.service_account import Credentials

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def authenticate_and_get_sheet():
    """URL과 인덱스를 사용하여 구글 시트의 첫 번째 탭을 연결하다."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 1. 설정 및 인증 파일 로드
    creds_path = os.path.join(BASE_DIR, "service_account.json")
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    
    # 2. 대안 2: 시트 URL로 직접 열기 (ID 입력 실수 방지)
    sheet_url = "https://docs.google.com/spreadsheets/d/1JTOOfZTaqImO4aQKEq1itcvggALuy4t5VYipuv4x3xo/edit"
    spreadsheet = client.open_by_url(sheet_url)
    
    # 3. 대안 1: 인덱스로 탭 가져오기 (이름 오타 문제 해결)
    # 0은 가장 왼쪽의 첫 번째 탭을 의미하다.
    worksheet = spreadsheet.get_worksheet(0)
    return worksheet

if __name__ == "__main__":
    try:
        print("🚀 구글 시트 연결을 시작합니다...")
        ws = authenticate_and_get_sheet()
        
        # 데이터 읽기 테스트
        data = ws.get_all_records()
        if data:
            target_store = data[0] # 첫 번째 데이터행(낙지마실)
            print(f"✅ 연결 성공: [{ws.title}] 탭을 읽어왔습니다.")
            print(f"📊 매장명: {target_store['shop_name']}")
            print(f"📍 지역: {target_store['region']}")
            print(f"📝 상황 분석: {target_store['situation1']}")
        
    except Exception as e:
        print(f"❌ 최종 연결 실패: {e}")
        print("💡 팁: 구글 시트의 '공유' 버튼을 눌러 서비스 계정 이메일이 추가되어 있는지 다시 확인하세요.")
