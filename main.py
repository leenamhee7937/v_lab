import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="AI 혈액 삼투압 실험실", layout="wide")

# --- 데이터 정의 ---
# 표준 데이터
standard_data = {
    "농도(%)": [0.1, 0.9, 3.0],
    "부피변화율(%)": [35, 0, -25],
    "상태": ["용혈 (파괴됨)", "정상 (원반형)", "수축 (고장액)"]
}
df_std = pd.DataFrame(standard_data)

# 미지 시료 데이터
unknown_samples = {
    "미지시료 X": {"volume": -15, "true_conc": 2.0, "hint": "부피가 15% 감소했습니다. 0.9%와 3.0% 사이를 확인하세요."},
    "미지시료 Y": {"volume": 20, "true_conc": 0.4, "hint": "부피가 20% 증가했습니다. 0.1%와 0.9% 사이를 확인하세요."}
}

# --- 세션 상태 초기화 ---
if 'visited' not in st.session_state:
    st.session_state.visited = set()
if 'show_line' not in st.session_state:
    st.session_state.show_line = False

# --- UI 레이아웃 ---
st.title("🔬 AI 기반 혈액 삼투압 가상 실험실")
st.markdown("용액의 농도에 따른 적혈구의 부피 변화를 관찰하고, 미지 시료의 농도를 정량 분석해 보세요.")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🧪 실험 제어판")
    
    # 버튼 배열
    btn_cols = st.columns(3)
    if btn_cols[0].button("0.1% NaCl (저장액)"): st.session_state.selected = 0.1
    if btn_cols[1].button("0.9% NaCl (식염수)"): st.session_state.selected = 0.9
    if btn_cols[2].button("3.0% NaCl (고장액)"): st.session_state.selected = 3.0
    
    unk_cols = st.columns(2)
    if unk_cols[0].button("미지시료 X"): st.session_state.selected = "미지시료 X"
    if unk_cols[1].button("미지시료 Y"): st.session_state.selected = "미지시료 Y"

    # 실험 결과 표시
    if 'selected' in st.session_state:
        sel = st.session_state.selected
        st.divider()
        
        if isinstance(sel, float):
            st.session_state.visited.add(sel)
            row = df_std[df_std["농도(%)"] == sel].iloc[0]
            st.info(f"**현재 용액:** NaCl {sel}%")
            st.metric("적혈구 부피 변화율", f"{row['부피변화율(%)']}%")
            st.warning(f"**세포 상태:** {row['상태']}")
        else:
            st.info(f"**현재 용액:** {sel}")
            st.metric("적혈구 부피 변화율", f"{unknown_samples[sel]['volume']}%")
            st.warning("**세포 상태:** 농도에 따른 부피 변화 발생")
            
            # 정답 입력 섹션
            with st.expander("❓ 미지시료 농도 맞추기", expanded=True):
                user_input = st.number_input("추정 농도(%)를 입력하세요", step=0.1, key="guess")
                if st.button("정답 확인"):
                    if abs(user_input - unknown_samples[sel]['true_conc']) < 0.01:
                        st.balloons()
                        st.success(f"정답입니다! {sel}의 농도는 {unknown_samples[sel]['true_conc']}%입니다.")
                    else:
                        st.error("틀렸습니다. 그래프의 검량선을 다시 확인해 보세요.")
                if st.session_state.show_line:
                    st.caption(f"💡 힌트: {unknown_samples[sel]['hint']}")

with col2:
    st.subheader("📈 농도-부피 변화율 그래프")
    
    # 그래프 생성
    fig = go.Figure()

    # 기준점 그리기 (방문한 점만)
    visited_df = df_std[df_std["농도(%)"].isin(st.session_state.visited)]
    fig.add_trace(go.Scatter(
        x=visited_df["농도(%)"], y=visited_df["부피변화율(%)"],
        mode='markers', name='측정 데이터',
        marker=dict(color='red', size=12)
    ))

    # 검량선 그리기
    if len(st.session_state.visited) == 3:
        if st.button("📊 표준 검량선(검은선) 그리기"):
            st.session_state.show_line = True
        
        if st.session_state.show_line:
            fig.add_trace(go.Scatter(
                x=df_std["농도(%)"], y=df_std["부피변화율(%)"],
                mode='lines', name='표준 검량선',
                line=dict(color='black', width=3)
            ))

    # 그래프 레이아웃 설정
    fig.update_layout(
        xaxis_title="NaCl 농도 (%)",
        yaxis_title="부피 변화율 (%)",
        xaxis=dict(range=[0, 3.5], gridcolor='lightgray'),
        yaxis=dict(range=[-45, 45], gridcolor='lightgray'),
        plot_bgcolor='white',
        height=500,
        showlegend=True
    )
    
    # 0점 기준선
    fig.add_hline(y=0, line_dash="dash", line_color="gray")

    st.plotly_chart(fig, use_container_width=True)
    
    if len(st.session_state.visited) < 3:
        st.caption("⚠️ 0.1%, 0.9%, 3.0% 데이터를 모두 확인하면 검량선을 그릴 수 있습니다.")

# --- 하단 설명 ---
st.divider()
st.markdown("""
### 📖 실험 가이드
1. 상단의 **NaCl 농도 버튼**을 눌러 각 환경에서 적혈구의 부피 변화를 측정합니다.
2. 모든 기준 농도(0.1, 0.9, 3.0)를 확인한 후 **검량선 그리기** 버튼을 누릅니다.
3. **미지시료**를 선택하고, 측정된 부피 변화율이 검량선의 어느 농도(X축)에 해당하는지 추론합니다.
""")
