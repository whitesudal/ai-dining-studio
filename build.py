import os
import json
import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

FALLBACK_HTML = """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>AI Dining Studio</title>
  <style>
    body{font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;line-height:1.6}
    code{background:#f6f8fa;padding:2px 6px;border-radius:6px}
    .card{border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin:12px 0}
    .muted{color:#6b7280}
  </style>
</head>
<body>
  <h1>AI Dining Studio</h1>
  <p class="muted">index.html 템플릿을 찾지 못해 기본 페이지로 생성한다.</p>

  <div class="card">
    <h2>빌드 상태</h2>
    <ul>
      <li>menu.yml: {menu_status}</li>
      <li>json 파일 수: {json_count}개</li>
      <li>출력: dist/index.html</li>
    </ul>
  </div>

  <div class="card">
    <h2>해결 방법</h2>
    <ol>
      <li>src/templates/index.html 을 레포에 추가한다.</li>
      <li>또는 templates/index.html 을 레포에 추가한다.</li>
    </ol>
  </div>
</body>
</html>
"""

def build_site():
    # 1) menu.yml 읽기 (없어도 진행)
    data_path = "data/menu.yml"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Using empty data.")
        menu_data = []
        menu_status = "없음, 빈 데이터로 진행"
    else:
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                menu_data = yaml.safe_load(f) or []
            menu_status = "로드 성공"
        except Exception as e:
            print(f"Error: menu.yml read failed ({type(e).__name__}). Using empty data.")
            menu_data = []
            menu_status = "읽기 오류, 빈 데이터로 진행"

    # 2) data 폴더의 json 개수 세기 (fallback에 표시용)
    json_count = 0
    if os.path.isdir("data"):
        json_count = len([fn for fn in os.listdir("data") if fn.endswith(".json")])

    # 3) dist 폴더 생성
    os.makedirs("dist", exist_ok=True)

    # 4) 템플릿 폴더 후보(둘 중 있으면 사용)
    template_dir = None
    for cand in ["src/templates", "templates"]:
        if os.path.isdir(cand):
            template_dir = cand
            break

    # 5) 템플릿 폴더 자체가 없으면 fallback 생성하고 종료(성공 처리)
    if template_dir is None:
        html = FALLBACK_HTML.format(menu_status=menu_status, json_count=json_count)
        with open("dist/index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Build ok: dist/index.html generated (template dir missing).")
        return

    # 6) 템플릿 로드 시도, 없으면 fallback 생성(성공 처리)
    env = Environment(loader=FileSystemLoader(template_dir))
    try:
        template = env.get_template("index.html")
    except TemplateNotFound:
        html = FALLBACK_HTML.format(menu_status=menu_status, json_count=json_count)
        with open("dist/index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Build ok: dist/index.html generated (index.html missing).")
        return

    # 7) 정상 렌더링
    output = template.render(menu=menu_data)

    # 8) dist/index.html 저장
    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Build ok: dist/index.html generated from template_dir='{template_dir}' and '{data_path}'.")

if __name__ == "__main__":
    build_site()
