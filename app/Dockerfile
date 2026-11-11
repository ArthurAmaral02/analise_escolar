FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/src/ ./src
copy app/dados ./dados

CMD ["tail", "-f", "/dev/null"]