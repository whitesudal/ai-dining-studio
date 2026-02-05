from pathlib import Path
import qrcode

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "site"
OUT.mkdir(exist_ok=True)

url = "http://localhost:8000"

img = qrcode.make(url)
img_path = OUT / "qr.png"
img.save(img_path)

print("QR 생성 완료:", img_path)
print("QR 접속 주소:", url)

