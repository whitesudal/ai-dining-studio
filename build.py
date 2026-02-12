import yaml
import os
from jinja2 import Environment, FileSystemLoader

def build_site():
    # [중요] 로봇이 가져온 'data/menu.yml' 파일을 읽도록 경로 수정
    data_path = 'data/menu.yml'
    
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Using empty data.")
        menu_data = []
    else:
        with open(data_path, 'r', encoding='utf-8') as f:
            menu_data = yaml.safe_load(f)

    # 템플릿 설정 (src/templates 폴더 기준)
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('index.html')

    # 결과물 생성
    output = template.render(menu=menu_data)

    # index.html 저장
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(output)
    print("Successfully built index.html from data/menu.yml")

if __name__ == "__main__":
    build_site()

