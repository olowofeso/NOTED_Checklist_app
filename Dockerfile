FROM python:3.11-slim

WORKDIR /app
COPY . .

# Install dependencies
RUN apt-get update \
    && apt-get install -y ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set Python path
ENV PYTHONPATH=/app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app ./app 

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]