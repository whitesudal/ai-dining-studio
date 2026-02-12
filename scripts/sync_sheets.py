import pandas as pd
import yaml
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# 설정 (구글 시트 탭 이름을 'data'로 설정 완료)
SHEET_ID = '1JTOOfZtaqImO4aQKEq1i6P3vFmDq6zVf39fSj0O4Lz4' 
SHEET_NAME = 'data' 

def sync():
    creds_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
    if not creds_json:
        print("Error: GOOGLE_SERVICE_ACCOUNT_JSON not found")
        return
    
    creds_info = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_info, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    service = build('sheets', 'v4', credentials=creds)
    
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=SHEET_NAME).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
        return

    df = pd.DataFrame(values[1:], columns=values[0])
    os.makedirs('src/data', exist_ok=True)
    with open('src/data/menu.yml', 'w', encoding='utf-8') as f:
        yaml.dump(df.to_dict(orient='records'), f, allow_unicode=True)
    print("Successfully updated menu.yml from 'data' sheet")

if __name__ == "__main__":
    sync()
