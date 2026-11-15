FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/src/ ./src
copy app/dados ./dados

CMD ["streamlit", "run", "interface/app.py", "--server.address=0.0.0.0", "--server.port=8080"]