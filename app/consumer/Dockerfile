FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV KAFKA_BROKER=kafka:9092
ENV MONGO_URI=mongodb://mongodb:27017/

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "consumer.py"]
