FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app2.py .

EXPOSE 9090

CMD ["python", "app2.py"]