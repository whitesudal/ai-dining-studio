import pandas as pd
import yaml
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# 설정 (이미지 60.jpg의 시트 정보와 일치함)
SHEET_ID = '1JTOOfZtaqImO4aQKEq1i6P3vFmDq6zVf39fSj0O4Lz4' 
SHEET_NAME = 'data' 

def sync():
    # GitHub Secrets에 등록된 구글 서비스 계정 키를 가져옴
    creds_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
    if not creds_json:
        print("Error: GOOGLE_SERVICE_ACCOUNT_JSON not found")
        return
    
    creds_info = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_info, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    service = build('sheets', 'v4', credentials=creds)
    
    # 구글 시트에서 데이터 읽기
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=SHEET_NAME).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found in Google Sheets.')
        return

    # 첫 번째 행을 제목으로 하여 데이터프레임 생성
    df = pd.DataFrame(values[1:], columns=values[0])
    
    # 빌드 시스템이 데이터를 읽어갈 수 있도록 data 폴더에 저장
    # 경로를 'data/menu.yml'로 지정하여 접근성을 높임
    os.makedirs('data', exist_ok=True)
    with open('data/menu.yml', 'w', encoding='utf-8') as f:
        yaml.dump(df.to_dict(orient='records'), f, allow_unicode=True)
        
    print("Successfully updated data/menu.yml from Google Sheets")

if __name__ == "__main__":
    sync()
