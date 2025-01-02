import streamlit as st
import requests
import time
import pandas as pd

API_URL = "http://172.17.0.1:3456"  # FastAPI 서버 주소

st.title("온도 및 습도 모니터링")

# 사이드바에 설정 추가
st.sidebar.header("설정")
update_interval = st.sidebar.slider("업데이트 간격(초)", 1, 30, 5)
max_data_points = st.sidebar.slider("표시할 최대 데이터 포인트", 10, 100, 30)

# 데이터를 저장할 리스트 초기화
data = []

# 그래프와 최신 데이터를 표시할 컨테이너 생성
chart = st.empty()
latest_data = st.empty()

while True:
    try:
        response = requests.get(f"{API_URL}/sensor")
        sensor_data = response.json()
        
        current_time = time.strftime("%H:%M:%S")
        data.append({
            "시간": current_time,
            "온도": sensor_data["temperature"],
            "습도": sensor_data["humidity"]
        })
        
        # 최대 데이터 포인트 수 유지
        if len(data) > max_data_points:
            data = data[-max_data_points:]
        
        # 데이터프레임 생성 및 차트 업데이트
        df = pd.DataFrame(data)
        chart.line_chart(df.set_index("시간"))
        
        # 최신 데이터 업데이트
        latest_data.metric(
            label="최신 데이터",
            value=f"온도: {sensor_data['temperature']}°C",
            delta=f"습도: {sensor_data['humidity']}%"
        )
        
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류 발생: {e}")
    
    time.sleep(update_interval)

# 수동으로 데이터 추가하는 기능
st.sidebar.header("수동 데이터 입력")
manual_temp = st.sidebar.number_input("온도 (°C)", -50.0, 50.0, 25.0, 0.1)
manual_humidity = st.sidebar.number_input("습도 (%)", 0.0, 100.0, 50.0, 0.1)

if st.sidebar.button("데이터 추가"):
    try:
        response = requests.post(
            f"{API_URL}/sensor",
            json={"temperature": manual_temp, "humidity": manual_humidity}
        )
        if response.status_code == 200:
            st.sidebar.success("데이터가 성공적으로 추가되었습니다.")
        else:
            st.sidebar.error("데이터 추가 실패")
    except Exception as e:
        st.sidebar.error(f"데이터 추가 중 오류 발생: {e}")