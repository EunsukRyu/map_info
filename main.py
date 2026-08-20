# main.py
import os
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. 웹 페이지 기본 설정
st.set_page_config(
    page_title="남동고 등산 메이트",
    page_icon="🌲",
    layout="wide"
)

st.title("🌳😁 2026 학교 등산 행사 안내 지도")
st.caption("우리 동아리가 직접 발로 뛰며 만든 코스 가이드입니다. 왼쪽 메뉴에서 코스를 선택하고 행사에 참여해 보세요!")

# 2. 데이터 불러오기
df = pd.read_csv('등산경로.csv', encoding='utf-8')
df['이미지'] = df['코스'] + df['위치명'] + '.jpg'

# 2-1. 코스별 세부 정보 사전 설정 (소요시간, 주의사항 등)
course_info = {
    "A코스": {
        "color": "blue",
        "time": "4~5분",
        "desc": "학교 출발",
        "notice": "경사가 완만하여 초보자에게 추천합니다.",
        "caution": "편안한 운동화를 착용하세요."
    },
    "B코스": {
        "color": "green",
        "time": "8~9분",
        "desc": "가온어린이공원 경유",
        "notice": "탁 트인 조망과 아름다운 자연 경관을 즐길 수 있습니다.",
        "caution": "낙엽 및 미끄럼 주의, 등산화 권장."
    },
    "C코스": {
        "color": "orange",
        "time": "10~11분",
        "desc": "서해랑길 94코스 출발",
        "notice": "접근성이 뛰어난 완주 코스입니다.",
        "caution": "수분 보충을 위해 물을 챙기세요."
    },
    "D코스": {
        "color": "red",
        "time": "13~14분",
        "desc": "세븐일레븐 코스",
        "notice": "편의점이 있어 간식 및 음료 구매가 편리합니다.",
        "caution": "쓰레기는 반드시 되가지고 내려오세요."
    },
    "E코스": {
        "color": "purple",
        "time": "12~13분",
        "desc": "논현주공1단지 코스",
        "notice": "입구를 잘 찾아가야하는 코스입니다.",
        "caution": "벌레에 물리지 않도록 벌레기피제 사용을 권장합니다."
    }
}

# 3. 사이드바 - 코스 선택 
st.sidebar.header("📌 코스 선택")

# Excel 데이터 내에 존재하는 실제 코스 목록 추출
unique_courses = list(df['코스'].unique()) if '코스' in df.columns else []
course_options = ["전체 코스 보기"] + unique_courses

selected_course = st.sidebar.selectbox("가고 싶은 코스를 선택하세요", course_options)

# 선택한 코스에 맞게 데이터 필터링
if selected_course == "전체 코스 보기":
    filtered_df = df.copy()
else:
    filtered_df = df[df['코스'] == selected_course].copy()

# 4. 지도 생성 및 중심점/줌레벨 자동 설정
#if not filtered_df.empty:
#    center_lat = filtered_df['위도'].mean()
#    center_lon = filtered_df['경도'].mean()
#    zoom_lvl = 15 if selected_course != "전체 코스 보기" else 13
#else:
    #center_lat, center_lon = 37.40583317, 126.7214872
    #zoom_lvl = 13

m = folium.Map(location=[37.40583317, 126.7214872], zoom_start=13)

# 4-1. 코스별 마커 및 경로 선(PolyLine) 시각화
for course_name, group in df.groupby('코스'):
    # 특정 코스가 선택된 경우 해당 코스만 그리기
    if selected_course != "전체 코스 보기" and course_name != selected_course:
        continue
    
    # 코스 식별 키 추출 (예: 'A코스(가온어린이공원)' -> 'A코스')
    c_key = course_name.split('(')[0].strip()
    c_data = course_info.get(c_key, {"color": "gray", "time": "-", "notice": "", "caution": "안전에 유의하세요."})
    marker_color = c_data["color"]
    
    # Points 선으로 잇기 (등산 경로 표시)
    path_points = group[['위도', '경도']].values.tolist()
    if len(path_points) > 1:
        folium.PolyLine(
            locations=path_points,
            color=marker_color,
            weight=4,
            opacity=0.8,
            tooltip=course_name
        ).add_to(m)

    # 지점별 마커 및 사진 팝업 추가
    for idx, row in group.iterrows():
        img_file = row['이미지']
        
        # Folium Popup HTML 작성 (지점명 + 코스 + 클릭 시 띄울 이미지)
        popup_html = f'''
        <div style="width:200px; text-align:center; font-family:sans-serif;">
            <h4 style="margin:5px 0; color:#2c3e50;">{row['위치명']}</h4>
            <p style="margin:2px; font-size:12px; color:#7f8c8d;">{row['코스']}</p>
            <hr style="margin:5px 0; border:0; border-top:1px solid #ddd;">
            <img src="{img_file}" width="180px" style="border-radius:6px; margin-top:5px;" onerror="this.onerror=null; this.src='https://via.placeholder.com/180x120?text=No+Image';">
        </div>
        '''
        
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"{row['위치명']} (클릭 시 상세/사진 보기)",
            icon=folium.Icon(color=marker_color, icon='info-sign')
        ).add_to(m)

# 5. 메인 레이아웃 (지도 & 우측 코스 상세 정보)
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🗺️ 등산 경로 지도")
    st_folium(m, width="100%", height=550)

with col2:
    st.subheader("ℹ️ 코스 상세 안내")
    
    if selected_course != "전체 코스 보기":
        c_key = selected_course.split('(')[0].strip()
        info = course_info.get(c_key, {})
        
        st.markdown(f"### 🚩 **{selected_course}**")
        st.info(f"🔔 {info.get('notice', '즐거운 등산 되세요!')}")
        st.metric(label="⏱️ 예상 소요시간", value=info.get('time', '-'))
        st.warning(f"💊 **주의사항**: {info.get('caution', '등산화를 착용하세요.')}")
        
        st.markdown("---")
        st.subheader("📸 지점별 포인트 사진")
        
        # 선택한 코스의 지점별 사진 목록 출력
        for idx, row in filtered_df.iterrows():
            st.write(f"📍 **{row['위치명']}**")
            img_path = row['이미지']
            if os.path.exists(img_path):
                st.image(img_path, caption=row['위치명'], use_container_width=True)
            else:
                st.caption("📷 *(해당 지점 이미지 파일 준비 중)*")
    else:
        st.info("👈 왼쪽 사이드바에서 특정 코스(A~E)를 선택하면 예상 소요시간, 주의사항 및 포인트별 사진을 상세히 보실 수 있습니다.")
        
        st.markdown("### 📋 전체 코스 개요")
        for k, v in course_info.items():
            st.markdown(f"- **{k}**: {v['desc']} *(소요시간: {v['time']})*")
            
        summary_list = []
        for c_code in unique_courses:
            c_df = df[df['코스'] == c_code]
            last_time = c_df[c_df['위치명'].str.contains('정상')]['소요시간'].values
            t_str = last_time[0] if len(last_time) > 0 else c_df.iloc[-1]['소요시간']
            summary_list.append({"코스": f"{c_code}코스", "총 소요시간(분:초)": t_str, "포인트 개수": len(c_df)})
        
        st.dataframe(pd.DataFrame(summary_list), hide_index=True, use_container_width=True)
        
            
"""
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

#1. 웹 페이지 설정
st.set_page_config(page_title="등산 메이트", layout="wide")

st.title("🏔️ 2026 학교 등산 행사 안내 지도")
st.markdown("우리 동아리가 직접 발로 뛰며 만든 코스 가이드입니다.")
st.markdown("왼쪽 메뉴에서 코스를 선택하고 행사에 참여해 보세요.")
st.markdown("# 큰 제목(Markdown)")
st.markdown("**굵은 글씨**와 *이탤릭체* 사용 가능")

st.header("헤더입니다.")
st.subheader("서브헤더입니다")
st.caption("캡션(설명)입니다.")
st.code(print('hello'), language='python')

#수식표시 
st.latex(r'''
a + a r^1 + a r^2 + a r^3 ''')

#데이터 읽어와 지도에 표시하기
df = pd.read_csv('인천광역시 남동구_고등학교_20240325.csv', encoding='cp949')
df_latlon = df[['위도', '경도']]
df_latlon = df_latlon.rename(columns={'위도':'lat', '경도':'lon'})
st.map(df_latlon)


#2. 데이터 준비 (데이터 가공 단계에서 학생들이 채울 부분)
# 실제로는 CSV나 GPX 파일을 불러오도록 해야, 테스트용으로 데이터를 직접 넣었습니다.
courses = {
    "A코스 (초급)": {"lat": 37.40583317, "lon": 126.7214872, "color": "blue", "desc": "경사가 완만하여 초보자에게 추천합니다."},
    "B코스 (중급)": {"lat": 37.40375712, "lon": 126.7270004, "color": "red", "desc": "계단이 많지만 경치가 매우 좋습니다."}
}

# 3. 사이드바 - 코스 선택 (if문 활용 실습 구간)
st.sidebar.header("📍 코스 선택")
selected_course = st.sidebar.selectbox("가고 싶은 코스를 선택하세요", list(courses.keys()))

# 4. 지도 생성 및 마커 표시 (지도 시각화 단계)
m = folium.Map(location=[37.40583317, 126.7214872], zoom_start=15)

# 선택된 코스 정보 가져오기
info = courses[selected_course]

# 지도에 마커 찍기 (반복문/if문 활용 가능)
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
"""
