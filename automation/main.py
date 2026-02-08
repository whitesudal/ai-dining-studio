import yaml
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import datetime

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

print("CONFIG LOADED:", config)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    config["google_credentials"], scope
)
client = gspread.authorize(creds)

sheet = client.open_by_key(
    config["google_sheet"]["sheet_id"]
).worksheet(
    config["google_sheet"]["worksheet_name"]
)

rows = sheet.get_all_records()
print("총 행 개수:", len(rows))

output_dir = config["paths"]["output_dir"]
os.makedirs(output_dir, exist_ok=True)

for idx, row in enumerate(rows, start=2):
    if row.get("status"):
        continue

    shop_name = str(row.get("shop_name", "no_name")).replace(" ", "_")
    filename = f"{shop_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(row))

    sheet.update_cell(idx, 17, "done")
    sheet.update_cell(idx, 18, filepath)

print("작업 완료")
