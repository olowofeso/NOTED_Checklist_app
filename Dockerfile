FROM python:3.11-slim

WORKDIR /app

# 1) Add CA certs so SSL handshakes succeed
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# 2) Copy & install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copy your code
COPY . .

# 4) Expose port and start Gunicorn against your real `app` object
EXPOSE 10000
ENTRYPOINT ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
