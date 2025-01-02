# Dockerfile
FROM python:3.11

WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 80 열기 (Streamlit 기본 포트)
EXPOSE 80

# HEALTHCHECK CMD curl --fail http://localhost/_stcore/health
# 실행 명령
CMD ["streamlit", "run", "app/main.py", "--server.address", "0.0.0.0", "--server.port", "80"]