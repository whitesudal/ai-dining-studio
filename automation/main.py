import os
import yaml
import gspread
from google.oauth2.service_account import Credentials

# 1. 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

def load_config():
    """YAML 설정 파일을 안전하게 로드합니다."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def authenticate_google_sheets(config):
    """구글 시트 인증을 수행하고 연결된 워크시트 객체를 반환합니다."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 설정 파일에 명시된 서비스 계정 키 경로 (service_account.json)
    creds_path = os.path.join(BASE_DIR, config["google_credentials"])
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    
    # 시트 ID와 '시트 1' 탭 이름을 사용하여 연결
    spreadsheet = client.open_by_key(config["google_sheet"]["sheet_id"])
    return spreadsheet.worksheet(config["google_sheet"]["worksheet_name"])

# --- 메인 실행부 ---
if __name__ == "__main__":
    config = load_config()
    print(f"⚙️  설정 로드 완료: {config['google_sheet']['worksheet_name']} 연결 시도 중...")

    try:
        # 구글 시트 연결
        ws = authenticate_google_sheets(config)
        print(f"✅ 성공: '{config['google_sheet']['worksheet_name']}' 탭에 정상적으로 연결되었습니다!")
        
        # 실제 데이터 가져오기
        all_data = ws.get_all_records()
        
        if all_data:
            print(f"📊 총 {len(all_data)}행의 데이터를 불러오는 데 성공했습니다.")
            print("\n--- 로드된 데이터 상세 ---")
            for i, row in enumerate(all_data):
                # 이미지 29번의 컬럼명을 기준으로 데이터 출력
                print(f"[{i+1}] 식당명: {row.get('shop_name', 'N/A')}")
                print(f"    📍 타겟: {row.get('audience', '정보 없음')}")
                print(f"    📝 목적: {row.get('purpose', '정보 없음')}")
                print(f"    ⭐ 점수: 혼밥({row.get('solo', 0)}) / 가족({row.get('family', 0)}) / 관광({row.get('tourist', 0)})")
        else:
            print("⚠️ 연결은 성공했으나 시트에 데이터가 비어 있습니다.")

    except Exception as e:
        print(f"❌ 최종 연결 실패: {e}")
        print("💡 팁: 시트 탭 이름 '시트 1'의 앞뒤에 숨겨진 공백이 없는지 다시 확인하세요.")import os
import yaml
import gspread
from google.oauth2.service_account import Credentials

# 1. 경로 

    try:
        # 구글 시트 연결 시도
        ws = authenticate_google_sheets(config)
        print(f"✅ 성공: '{config['google_sheet']['worksheet_name']}' 연결 완료하다.")
        
        # 데이터 전체 로드
        data = ws.get_all_records()
        print(f"📊 로드된 데이터 수: {len(data)}행")
        
        # 데이터가 존재할 경우 화면에 출력하다.
        if data:
            print("\n--- 로드된 데이터 상세 ---")
            for i, row in enumerate(data):
                print(f"[{i+1}번 식당]: {row['shop_name']}")
                print(f" - 타겟: {row['audience']}")
                print(f" - 목적: {row['purpose']}")
                print(f" - 점수: Solo({row['solo']}), Family({row['family']}), Tourist({row['tourist']})")

    except Exception as e:
        print(f"❌ 연결 실패 상세 사유: {e}")
        print("팁: 구글 시트 하단 탭 이름이 정확히 '시트 1'인지 확인하다.")
