FROM python:3.13-slim

WORKDIR /app

# Install ping utility
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*

COPY . .

# Install Python dependencies
RUN pip install flask pandas openpyxl

# Enable Flask debug mode
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

EXPOSE 5000

CMD ["sh", "-c", "python scripts/daily_scan_docker.py && python monitor/monitor.py"]
