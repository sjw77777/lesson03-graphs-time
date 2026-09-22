import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")

st.write(
    "1년치 일별 박스오피스 데이터를 이용해 영화의 관객 변화를 살펴봅니다."
)

# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

df = pd.read_csv(DATA_URL)

# 날짜를 진짜 날짜 형식으로 변환
df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")

# 일관객을 숫자로 변환
df["일관객"] = pd.to_numeric(df["일관객"], errors="coerce")

# 날짜순으로 정렬
df = df.sort_values("날짜")


# ==================================================
# 그래프 1
# ==================================================
st.header("그래프 1. 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화의 날짜별 일관객 변화를 확인할 수 있습니다."
)

# 영화 목록
movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

# 선택한 영화 데이터
movie_df = df[df["영화명"] == selected_movie].copy()

movie_df = movie_df.sort_values("날짜")

# Plotly 선 그래프
fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}'의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,.0f"
    }
)

fig.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,.0f}명<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# 그래프 설명
st.subheader("이 그래프로 알 수 있는 것")

st.text_input(
    "이 그래프로 알 수 있는 것을 입력하세요.",
    placeholder="예: 영화의 개봉 이후 일관객 수가 어떻게 변화했는지 알 수 있다.",
    key="graph1_explanation"
)


# ==================================================
# 앞으로 추가할 그래프 영역
# ==================================================
st.divider()

st.header("그래프 2")

st.info("앞으로 새로운 그래프를 추가할 공간입니다.")


st.divider()

st.header("그래프 3")

st.info("앞으로 새로운 그래프를 추가할 공간입니다.")
