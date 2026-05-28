import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. Streamlit 앱 화면 페이지 설정
st.set_page_config(
    page_title="AI 활용 혈액 삼투압 가상 실험실",
    page_icon="🔬",
    layout="wide"
)

# 2. 파이썬 문법 충돌을 원천 차단하기 위해 바이트 스트림 단위로 HTML 소스 분할 정의
html_segments = [
    b"<!DOCTYPE html><html lang=\"ko\"><head><meta charset=\"UTF-8\"><title>\xec\x95\x84\xec\x9d\xb4 \xed\x99\x9c\xec\x9a\xa9 \xed\x98\x88\xec\x95\xa1 \xec\x82\xbc\xed\x8a\xac\xec\x95\x9d \xea\xb0\x80\xec\x83\x81 \xec\x8b\xa4\xed\x97\x98\xec\x8b\xa4</title><style>",
    b"body { font-family: 'Malgun Gothic', sans-serif; background-color: #f5f7fa; margin: 0; padding: 20px; color: #333; }",
    b".container { max-width: 1000px; margin: 0 auto; background: #fff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }",
    b"h1 { text-align: center; color: #2c3e50; margin-bottom: 30px; }",
    b".control-panel { display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; flex-wrap: wrap; }",
    b"button { padding: 12px 24px; font-size: 15px; font-weight: bold; border: none; border-radius: 8px; cursor: pointer; transition: all 0.3s; }",
    b".btn-sample { background-color: #e2e8f0; color: #4a5568; } .btn-sample:hover { background-color: #cbd5e1; } .btn-sample.active { background-color: #3182ce; color: white; }",
    b"#btn-graph { background-color: #10b981; color: white; display: none; } #btn-graph:hover { background-color: #059669; }",
    b".lab-space { display: flex; justify-content: space-around; align-items: center; background: #edf2f7; padding: 30px; border-radius: 10px; min-height: 260px; margin-bottom: 30px; }",
    b".beaker { width: 180px; height: 200px; border: 5px solid #718096; border-top: none; border-radius: 0 0 15px 15px; position: relative; background: #ffffff; overflow: hidden; }",
    b".liquid { position: absolute; bottom: 0; width: 100%; height: 140px; background: rgba(66, 153, 225, 0.4); transition: background 0.5s; }",
    b".cell-container { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); display: flex; justify-content: center; align-items: center; }",
    b".red-blood-cell { width: 70px; height: 70px; background-color: #e53e3e; border-radius: 50%; box-shadow: inset 0 0 15px rgba(0,0,0,0.4); transition: all 1.5s ease-in-out; display: flex; justify-content: center; align-items: center; color: white; font-size: 11px; font-weight: bold; text-align: center; }",
    b".cell-crenated { width: 45px; height: 45px; border-radius: 35% 45% 35% 45%; background-color: #9b2c2c; } .cell-swollen { width: 95px; height: 95px; }",
    b".cell-lysed { width: 100px; height: 100px; background-color: rgba(229, 62, 62, 0.15); border: 2px dashed #e53e3e; box-shadow: none; color: #e53e3e; }",
    b".dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; } .info-box, .graph-box { background: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; }",
    b".info-item { margin-bottom: 12px; font-size: 16px; } .info-value { font-weight: bold; color: #2b6cb0; }",
    b".graph-wrapper { position: relative; width: 400px; height: 300px; margin: 10px auto; display: none; }",
    b"canvas { background: #ffffff; border-left: 2px solid #333; border-bottom: 2px solid #333; position: absolute; left: 50px; top: 20px; z-index: 1; }",
    b".axis-title-x { position: absolute; bottom: -15px; left: 220px; font-weight: bold; font-size: 12px; } .axis-title-y { position: absolute; left: -10px; top: 10px; font-weight: bold; font-size: 12px; }",
    b".label-text { position: absolute; font-size: 11px; color: #444; font-family: sans-serif; }",
    b".input-zone { margin-top: 15px; display: flex; gap: 10px; align-items: center; } input[type=\"number\"] { padding: 6px; width: 80px; border: 1px solid #cbd5e1; border-radius: 4px; }",
    b"#hint-box { margin-top: 10px; padding: 10px; background: #e0f2fe; border-radius: 4px; font-size: 13px; display: none; line-height: 1.4; }",
    b"</style></head><body><div class=\"container\"><h1>\xf0\x9f\x94
