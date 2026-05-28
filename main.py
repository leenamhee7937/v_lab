import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit 화면 레이아웃 폭 확장
st.set_page_config(layout="wide")

# 2. 같은 경로에 있는 index.html 파일 읽기
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # 3. HTML 콘텐츠를 Streamlit 컴포넌트 웹 화면에 삽입
    # 가상 실험실 콘텐츠 크기에 맞춰 높이(height)를 850으로 설정했습니다.
    components.html(html_content, height=850, scrolling=True)

except FileNotFoundError:
    st.error("⚠️ 'index.html' 파일을 찾을 수 없습니다. 파이썬 파일(main.py)과 같은 폴더에 위치해 있는지 확인해 주세요.")
