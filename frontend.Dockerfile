FROM python:3.13-slim

WORKDIR /app

RUN pip install streamlit httpx

COPY ./frontend ./frontend

EXPOSE 8501

CMD ["streamlit","run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
