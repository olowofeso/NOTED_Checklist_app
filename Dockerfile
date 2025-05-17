FROM python:3.11-slim

WORKDIR /app
COPY . .

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Set Python path
ENV PYTHONPATH=/app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app ./app 

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0:5000", "app:create_app"]