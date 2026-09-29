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
DATA_URL = "https://raw.githubusercontent.com/happykth/data/main/kobis_daily.csv"

df = pd.read_csv(DATA_URL)

# 날짜를 진짜 날짜 형식으로 변환
df["날짜"] = pd.to_datetime(
    df["날짜"].astype(str),
    format="%Y%m%d"
)

# 숫자 데이터 변환
df["일관객"] = pd.to_numeric(df["일관객"], errors="coerce")

# 날짜순 정렬
df = df.sort_values("날짜")


# ==================================================
# 그래프 1
# ==================================================
st.header("그래프 1. 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화의 날짜별 일관객 변화를 확인할 수 있습니다."
)

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}'의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,.0f}명<extra></extra>"
)

fig1.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.subheader("이 그래프로 알 수 있는 것")

st.text_input(
    "이 그래프로 알 수 있는 것을 입력하세요.",
    placeholder="예: 영화의 날짜별 일관객 수가 어떻게 변화했는지 알 수 있다.",
    key="graph1_explanation"
)


# ==================================================
# 그래프 2
# ==================================================
st.divider()

st.header("그래프 2. 일관객 합계가 가장 큰 영화 5편의 변화")

st.write(
    "전체 기간 동안 일관객 합계가 가장 큰 영화 5편의 날짜별 관객 변화를 비교합니다."
)

top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)
)

top5_movie_names = top5_movies["영화명"].tolist()

top5_df = df[
    df["영화명"].isin(top5_movie_names)
].copy()

top5_df = top5_df.sort_values(
    ["날짜", "영화명"]
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    title="일관객 합계 TOP 5 영화의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.caption(
    "범례에서 영화 이름을 클릭하면 해당 영화의 그래프를 켜거나 끌 수 있습니다."
)

st.subheader("이 그래프로 알 수 있는 것")

st.text_input(
    "이 그래프로 알 수 있는 것을 입력하세요.",
    placeholder="예: 기간 전체에서 관객 수가 많았던 영화들의 날짜별 관객 변화를 비교할 수 있다.",
    key="graph2_explanation"
)


# ==================================================
# 그래프 3
# ==================================================
st.divider()

st.header("그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "각 날짜의 박스오피스 10위권 영화들의 일관객을 모두 합산하여 날짜별 관객 규모를 보여 줍니다."
)

# 날짜별 10위권 일관객 합계
daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 3일
top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("날짜")
)

# 영역 그래프
fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)

# 전체 날짜별 데이터 hover
fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>10위권 일관객 합계: %{y:,.0f}명"
        "<extra></extra>"
    )
)

# 가장 큰 3일 표시
for _, row in top3_days.iterrows():

    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=(
            f"{row['날짜'].strftime('%Y-%m-%d')}"
            f"<br>{row['일관객']:,.0f}명"
        ),
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-50
    )

fig3.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.caption(
    "그래프 위에 표시된 날짜는 10위권 일관객 합계가 가장 컸던 3일입니다."
)

st.subheader("이 그래프로 알 수 있는 것")

st.text_input(
    "이 그래프로 알 수 있는 것을 입력하세요.",
    placeholder="예: 날짜에 따라 전체적인 영화 관객 규모가 어떻게 달라졌는지 알 수 있다.",
    key="graph3_explanation"
)


# ==================================================
# 앞으로 추가할 그래프 영역
# ==================================================
st.divider()

st.header("그래프 4")

st.info("앞으로 새로운 그래프를 추가할 공간입니다.")

# ==================================================
# 그래프 4
# ==================================================
st.divider()

st.header("그래프 4. 영화별 일관객 합계 TOP 10")

st.write(
    "전체 기간 동안 각 영화의 일관객을 모두 더해 관객 수가 많은 영화 TOP 10을 보여 줍니다."
)

# 영화별 일관객 합계
movie_total = (
    df.groupby("영화명")
    .agg(
        총일관객=("일관객", "sum"),
        top10일수=("날짜", "nunique")
    )
    .reset_index()
)

# 일관객 합계가 큰 TOP 10
top10_movies = (
    movie_total
    .sort_values("총일관객", ascending=False)
    .head(10)
    .sort_values("총일관객", ascending=True)
)

# 가로 막대그래프
fig4 = px.bar(
    top10_movies,
    x="총일관객",
    y="영화명",
    orientation="h",
    title="영화별 일관객 합계 TOP 10",
    labels={
        "총일관객": "기간 내 일관객 합계",
        "영화명": "영화"
    },
    custom_data=["top10일수"]
)

# 마우스를 올렸을 때 표시할 정보
fig4.update_traces(
    hovertemplate=(
        "영화: %{y}"
        "<br>일관객 합계: %{x:,.0f}명"
        "<br>10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="기간 내 일관객 합계(명)",
    yaxis_title="영화",
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.caption(
    "막대에 마우스를 올리면 영화별 일관객 합계와 10위권에 든 날수를 확인할 수 있습니다."
)

st.subheader("이 그래프로 알 수 있는 것")

st.text_input(
    "이 그래프로 알 수 있는 것을 입력하세요.",
    placeholder="예: 전체 기간 동안 누적 관객이 많았던 영화와 10위권에 오래 머문 영화를 확인할 수 있다.",
    key="graph4_explanation"
)


# ==================================================
# 앞으로 추가할 그래프 영역
# ==================================================
st.divider()

st.header("그래프 5")

st.info("앞으로 새로운 그래프를 추가할 공간입니다.")

# ==================================================
# 그래프 5
# ==================================================
st.divider()

st.header("그래프 5. 월 × 요일별 일관객 합계")

st.write(
    "월과 요일에 따라 박스오피스 10위권의 일관객 합계가 어떻게 달라지는지 보여 줍니다."
)

# 월 추출
df["월"] = df["날짜"].dt.month

# 요일 추출
weekday_map = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일"
}

df["요일"] = df["날짜"].dt.weekday.map(weekday_map)

# 요일 순서 지정
weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

df["요일"] = pd.Categorical(
    df["요일"],
    categories=weekday_order,
    ordered=True
)

# 월 × 요일별 일관객 합계
heatmap_data = (
    df.groupby(
        ["월", "요일"],
        observed=False
    )["일관객"]
    .sum()
    .reset_index()
)

# 피벗 테이블 생성
heatmap_pivot = heatmap_data.pivot(
    index="월",
    columns="요일",
    values="일관객"
)

# 월 순서 지정
heatmap_pivot = heatmap_pivot.reindex(range(1, 13))

# 히트맵
fig5 = px.imshow(
    heatmap_pivot,
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계"
    },
    x=weekday_order,
    y=[f"{month}월" for month in range(1, 13)],
    aspect="auto",
    color_continuous_scale="Blues",
    title="월 × 요일별 박스오피스 10위권 일관객 합계"
)

fig5.update_traces(
    hovertemplate=(
        "월: %{y}"
        "<br>요일: %{x}"
        "<br>일관객 합계: %{z:,.0f}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.caption(
    "색이 진할수록 해당 월·요일에 10위권 영화들의 일관객 합계가 많았다는 뜻입니다."
)

st.subheader("이 그래프로 알 수 있는 것")

st.text_input(
    "이 그래프로 알 수 있는 것을 입력하세요.",
    placeholder="예: 어느 월과 요일에 영화 관객이 많았는지 한눈에 비교할 수 있다.",
    key="graph5_explanation"
)


# ==================================================
# 앞으로 추가할 그래프 영역
# ==================================================
st.divider()

st.header("그래프 6")

st.info("앞으로 새로운 그래프를 추가할 공간입니다.")
