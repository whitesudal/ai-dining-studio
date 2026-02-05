from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data" / "restaurants"
TEMPLATES = ROOT / "templates"
OUT = ROOT / "site"

def load_restaurants():
    restaurants = []
    for p in sorted(DATA_DIR.glob("*.yaml")):
        r = yaml.safe_load(p.read_text(encoding="utf-8"))
        r["_file"] = p.name
        restaurants.append(r)
    return restaurants

def main():
    OUT.mkdir(exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)))
    restaurants = load_restaurants()
    html = env.get_template("index.html").render(restaurants=restaurants)
    (OUT / "index.html").write_text(html, encoding="utf-8")
    print("페이지 생성 완료:", OUT / "index.html")
    print("식당 수:", len(restaurants))

if __name__ == "__main__":
    main()

 
