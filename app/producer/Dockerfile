FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and data
COPY . /app
COPY data_file.pkl /app/

CMD ["python", "producer.py"]