import streamlit as st
import streamlit.components.v1 as components
import os

# 1. 화면 레이아웃 폭 확장
st.set_page_config(layout="wide")

# 2. 현재 main.py 파일이 있는 폴더의 절대 경로를 계산
current_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(current_dir, "index.html")

# 3. index.html 파일이 정상적으로 존재하면 읽어와서 실행
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # 가상 가상 실험실 콘텐츠 높이에 맞춰 height를 850으로 설정
    components.html(html_content, height=850, scrolling=True)
else:
    # 만약 배포 환경에서 파일을 여전히 못 찾을 경우, 디버깅 메시지를 화면에 표시
    st.error("⚠️ 'index.html' 파일을 찾을 수 없습니다.")
    st.info(f"현재 시스템이 탐색 중인 경로: {html_path}")
    st.info(f"현재 폴더 내에 존재하는 파일 목록: {os.listdir(current_dir)}")
