FROM python:3.13-slim

WORKDIR /app

# Install ping utility
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install flask

EXPOSE 5000

CMD ["sh", "-c", "python scripts/daily_scan_docker.py && python monitor/monitor.py"]
