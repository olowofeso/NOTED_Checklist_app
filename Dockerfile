FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create instance directory explicitly
RUN mkdir -p /app/instance && \
    chmod -R 777 /app/instance

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]