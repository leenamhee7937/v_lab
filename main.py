import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. Streamlit 앱 화면 페이지 설정
st.set_page_config(
    page_title="AI 활용 혈액 삼투압 가상 실험실",
    page_icon="🔬",
    layout="wide"
)

# 2. 독립적으로 완벽 구동되는 순수 HTML/CSS/JS 소스 코드
pure_html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>AI 활용 혈액 삼투압 가상 실험실</title>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; background-color: #f5f7fa; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 1000px; margin: 0 auto; background: #fff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #2c3e50; margin-bottom: 30px; }
        .control-panel { display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; flex-wrap: wrap; }
        button { padding: 12px 24px; font-size: 15px; font-weight: bold; border: none; border-radius: 8px; cursor: pointer; transition: all 0.3s; }
        .btn-sample { background-color: #e2e8f0; color: #4a5568; }
        .btn-sample:hover { background-color: #cbd5e1; }
        .btn-sample.active { background-color: #3182ce; color: white; }
        
        #btn-graph { background-color: #10b981; color: white; display: none; }
        #btn-graph:hover { background-color: #059669; }

        .lab-space { display: flex; justify-content: space-around; align-items: center; background: #edf2f7; padding: 30px; border-radius: 10px; min-height: 260px; margin-bottom: 30px; }
        .beaker { width: 180px; height: 200px; border: 5px solid #718096; border-top: none; border-radius: 0 0 15px 15px; position: relative; background: #ffffff; overflow: hidden; }
        .liquid { position: absolute; bottom: 0; width: 100%; height: 140px; background: rgba(66, 153, 225, 0.4); transition: background 0.5s; }
        .cell-container { position: absolute; top: 40%; left: 50%; transform: translate(-50
