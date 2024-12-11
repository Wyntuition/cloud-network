FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV KAFKA_BROKER=kafka:9092
ENV MONGO_URI=mongodb://mongodb:27017/

RUN apt-get update && apt-get install -y libgl1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

CMD ["python", "consumer.py"]
