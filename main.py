import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit 앱 화면 페이지 설정 (최대 폭 확장 및 타이틀 부여)
st.set_page_config(
    page_title="AI 활용 혈액 삼투압 가상 실험실",
    page_icon="🔬",
    layout="wide"
)

# 2. 독립적으로 완벽 구동되는 HTML/CSS/JS 소스 코드 정의
html_source = """
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
        .cell-container { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); display: flex; justify-content: center; align-items: center; }
        .red-blood-cell { width: 70px; height: 70px; background-color: #e53e3e; border-radius: 50%; box-shadow: inset 0 0 15px rgba(0,0,0,0.4); transition: all 1.5s ease-in-out; display: flex; justify-content: center; align-items: center; color: white; font-size: 11px; font-weight: bold; text-align: center; }
        .cell-crenated { width: 45px; height: 45px; border-radius: 35% 45% 35% 45%; background-color: #9b2c2c; }
        .cell-swollen { width: 95px; height: 95px; }
        .cell-lysed { width: 100px; height: 100px; background-color: rgba(229, 62, 62, 0.15); border: 2px dashed #e53e3e; box-shadow: none; color: #e53e3e; }

        .dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .info-box, .graph-box { background: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; }
        .info-item { margin-bottom: 12px; font-size: 16px; }
        .info-value { font-weight: bold; color: #2b6cb0; }
        
        .graph-wrapper { position: relative; width: 400px; height: 300px; margin: 10px auto; display: none; }
        canvas { background: #ffffff; border-left: 2px solid #333; border-bottom: 2px solid #333; position: absolute; left: 50px; top: 20px; z-index: 1; }
        .axis-title-x { position: absolute; bottom: -15px; left: 220px; font-weight: bold; font-size: 12px; }
        .axis-title-y { position: absolute; left: -10px; top: 10px; font-weight: bold; font-size: 12px; }
        .label-text { position: absolute; font-size: 11px; color: #444; font-family: sans-serif; }

        .input-zone { margin-top: 15px; display: flex; gap: 10px; align-items: center; }
        input[type="number"] { padding: 6px; width: 80px; border: 1px solid #cbd5e1; border-radius: 4px; }
        #hint-box { margin-top: 10px; padding: 10px; background: #e0f2fe; border-radius: 4px; font-size: 13px; display: none; line-height: 1.4; }
    </style>
</head>
<body>

<div class="container">
    <h1>🔬 오차 없는 AI 기반 혈액 삼투압 가상 실험실</h1>
    
    <div class="control-panel">
        <button class="btn-sample" onclick="selectSolution('0.1%', 0.1)">0.1% NaCl (저장액)</button>
        <button class="btn-sample" onclick="selectSolution('0.9%', 0.9)">0.9% NaCl (생리식염수)</button>
        <button class="btn-sample" onclick="selectSolution('3.0%', 3.0)">3.0% NaCl (고장액)</button>
        <button class="btn-sample" onclick="selectSolution('미지시료 X', 'unknown_X')">미지시료 X</button>
        <button class="btn-sample" onclick="selectSolution('미지시료 Y', 'unknown_Y')">미지시료 Y</button>
        <button id="btn-graph" onclick="drawCalibrationLine()">검은선(표준 검량선) 그리기</button>
    </div>

    <div class="lab-space">
        <div>
            <h3 style="text-align: center;" id="current-sol-
