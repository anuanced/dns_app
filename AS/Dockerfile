FROM python:3.11-slim

WORKDIR /app

COPY app.py .
COPY DNSrecords.json .

EXPOSE 53533/udp

CMD ["python", "app.py"]