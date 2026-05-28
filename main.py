import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit 앱 화면 페이지 설정
st.set_page_config(
    page_title="AI 활용 혈액 삼투압 가상 실험실",
    page_icon="🔬",
    layout="wide"
)

# 2. 앞에 'r'을 붙여 내부 특수문자(\n 등) 충돌을 방지한 HTML 소스 코드
html_source = r"""
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
            <h3 style="text-align: center;" id="current-sol-title">용액을 선택하세요</h3>
            <div class="beaker">
                <div class="liquid"></div>
                <div class="cell-container">
                    <div class="red-blood-cell" id="rbc">적혈구</div>
                </div>
            </div>
        </div>
    </div>

    <div class="dashboard">
        <div class="info-box">
            <h3>📊 정량 데이터 실시간 분석</h3>
            <div class="info-item">선택된 용액 농도: <span id="data-conc" class="info-value">-</span></div>
            <div class="info-item">적혈구 부피 변화율: <span id="data-volume" class="info-value">-</span></div>
            <div class="info-item">세포 상태 관찰: <span id="data-state" class="info-value">대기 중</span></div>
            
            <div class="input-zone" id="quiz-zone" style="display:none; flex-direction:column; align-items:flex-start;">
                <div style="display:flex; gap:10px; align-items:center;">
                    <label id="quiz-label">미지시료 농도 예측(%): </label>
                    <input type="number" id="user-guess" step="0.1">
                    <button onclick="checkAnswer()" style="padding: 6px 12px; background:#3182ce; color:white;">확인</button>
                </div>
                <div id="hint-box"></div>
            </div>
        </div>

        <div class="graph-box">
            <h3>📈 농도-부피 변화율 그래프</h3>
            <p style="font-size: 13px; color: #666;">기준 농도(0.1%, 0.9%, 3.0%) 데이터를 모두 확인하면 그래프가 나타납니다.</p>
            
            <div class="graph-wrapper" id="graph-wrapper">
                <div class="axis-title-x">NaCl 농도 (%)</div>
                <div class="axis-title-y">부피 변화율 (%)</div>
                
                <div class="label-text" style="left: 15px; top: 13px;">+40</div>
                <div class="label-text" style="left: 15px; top: 63px;">+20</div>
                <div class="label-text" style="left: 22px; top: 113px;">0</div>
                <div class="label-text" style="left: 11px; top: 163px;">-20</div>
                <div class="label-text" style="left: 11px; top: 213px;">-40</div>
                
                <div class="label-text" style="left: 58px; bottom: 10px;">0.1</div>
                <div class="label-text" style="left: 138px; bottom: 10px;">0.9</div>
                <div class="label-text" style="left: 218px; bottom: 10px;">1.7</div>
                <div class="label-text" style="left: 298px; bottom: 10px;">2.5</div>
                <div class="label-text" style="left: 348px; bottom: 10px;">3.0</div>

                <canvas id="graphCanvas" width="320" height="220"></canvas>
            </div>
        </div>
    </div>
</div>

<script>
    const dataset = {
        0.1: { volume: "+35% (용혈)", state: "세포 팽창 후 세포막 파괴 (용혈 현상)", class: "cell-lysed", cx: 10, cy: 32.5 },
        0.9: { volume: "0% (변화 없음)", state: "정상 상태 유지 (원반 모양)", class: "", cx: 90, cy: 120 },
        3.0: { volume: "-25% (수축)", state: "세포 내 수분 유출로 세포 수축", class: "cell-crenated", cx: 300, cy: 182.5 },
        'unknown_X': { volume: "-15% (수축)", state: "세포가 수축됨 (고장액 추정)", class: "cell-crenated", hint: "📊 [정량 추론 힌트]\n그래프 Y축의 부피 변화율 '-15%' 지점에서 가로로 쭉 이동해 보세요.\n검은선과 만나는 지점의 X축 농도 수치는 얼마인가요?" },
        'unknown_Y': { volume: "+20% (팽창)", state: "세포가 부풀어 오름 (저장액 추정)", class: "cell-swollen", hint: "📊 [정량 추론 힌트]\n그래프 Y축의 부피 변화율 '+20%' 지점에서 가로로 쭉 이동해 보세요.\n검은선과 만나는 지점의 X축 농도 수치는 얼마인가요?" }
    };

    let visitedPoints = new Set();
    let
