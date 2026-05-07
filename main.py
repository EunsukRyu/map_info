# main.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

#1. 웹 페이지 설정
st.set_page_config(page_title="등산 메이트", layout="wide")

st.title("🏔️ 2026 학교 등산 행사 안내 지도")
st.markdown("우리 동아리가 직접 발로 뛰며 만든 코스 가이드입니다.")
st.markdown("왼쪽 메뉴에서 코스를 선택하고 행사에 참여해 보세요.")

#2. 데이터 준비 (데이터 가공 단계에서 학생들이 채울 부분)
# 실제로는 CSV나 GPX 파일을 불러오도록 해야, 테스트용으로 데이터를 직접 넣었습니다.
courses = {
    "A코스 (초급)": {"lat": 37.40583317, "lon": 126.7214872, "color": "blue", "desc": "경사가 완만하여 초보자에게 추천합니다."},
    "B코스 (중급)": {"lat": 37.40375712, "lon": 126.7270004, "color": "red", "desc": "계단이 많지만 경치가 매우 좋습니다."}
}

# 3. 사이드바 - 코스 선택 (if문 활용 실습 구간)
st.sidebar.header("📍 코스 선택")
selected_course = st.sidebar.selectbox("가고 싶은 코스를 선택하세요", list(courses.keys()))

# 4. 지도 생성 및 마커 표시 (7월 커리큘럼: 지도 시각화 단계)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=15)

# 선택된 코스 정보 가져오기
info = courses[selected_course]

# 지도에 마커 찍기 (반복문/if문 활용 교육 가능)
folium.Marker(
    [info["lat"], info["lon"]],
    popup=selected_course,
    tooltip=f"{selected_course} 시작점",
    icon=folium.Icon(color=info["color"], icon="info-sign")
).add_to(m)

# 5. 화면 출력
col1, col2 = st.columns([3, 1])

with col1:
    st_folium(m, width=700, height=500)

with col2:
    st.subheader(f"[{selected_course}] 정보")
    st.info(info["desc"])
    st.metric(label="예상 소요 시간", value="40분")
    st.write("⚠️ 주의사항: 등산화를 꼭 착용하세요!")

