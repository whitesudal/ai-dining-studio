import os
import yaml
import gspread
from google.oauth2.service_account import Credentials

# 1. 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

def load_config():
    """YAML 설정 파일을 로드하여 딕셔너리로 반환하다."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
            return config_data if config_data else {}
    except FileNotFoundError:
        print(f"오류: 설정 파일을 찾을 수 없다. 경로: {CONFIG_PATH}")
        return {}

def authenticate_google_sheets(config):
    """구글 시트 API 인증 및 워크시트 객체를 반환하다."""
    # 인증 범위 설정
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 이미지 16번에서 확인한 파일명과 경로를 조합하다.
    creds_path = os.path.join(BASE_DIR, config["google_credentials"])
    
    # 서비스 계정 파일로 인증 수행
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    
    # 시트 ID와 워크시트 이름을 사용하여 연결하다.
    sheet_id = config["google_sheet"]["sheet_id"]
    worksheet_name = config["google_sheet"]["worksheet_name"]
    
    return client.open_by_key(sheet_id).worksheet(worksheet_name)

# --- 실행부: 데이터를 읽어와 화면에 출력하다 ---
if __name__ == "__main__":
    # 1단계: 설정 로드 확인.
    config = load_config()
    print(f"CONFIG LOADED: {config}")

    if not config:
        print("오류: 설정을 불러오지 못해 프로그램을 종료하다.")
    else:
        try:
            # 2단계: 구글 시트 연결 시도
            ws = authenticate_google_sheets(config)
            print(f"✅ 성공: '{config['google_sheet']['worksheet_name']}' 시트에 연결되다.")
            
            # 3단계: get_all_records()를 사용하여 전체 데이터 읽기
            # 시트의 첫 번째 행을 제목(Key)으로 삼아 데이터를 가져오다.
            all_rows = ws.get_all_records()
            
            print(f"📊 로드된 데이터 수: 총 {len(all_rows)}행")
            
            # 4단계: 화면에 출력 (데이터가 있을 경우 첫 3행만 샘플 출력)
            if all_rows:
                print("\n--- 데이터 샘플 (최대 3행) ---")
                for i, row in enumerate(all_rows[:3]):
                    print(f"[{i+1}행]: {row}")
            else:
                print("알림: 시트에 데이터가 비어 있다.")

        except Exception as e:
            # 인증 오류나 시트 ID 오류 발생 시 출력하다.
            print(f"❌ 구글 시트 연결 또는 데이터 읽기 실패: {e}")
            print("팁: 'sheet-bot@ai-dining-auto.iam.gserviceaccount.com' 이메일이 시트에 공유되었는지 확인하다.")
