import os
import time
from kafka import KafkaProducer
import sys
import threading
import pickle
import json
import uuid
import numpy as np

sent_messages = {}
lock = threading.Lock()

def consumer_thread_function(bootstrap_servers, consumer_topic):
    from kafka import KafkaConsumer
    consumer = KafkaConsumer(
        consumer_topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=str(uuid.uuid4()),
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    print("Starting consumer thread on topic ", consumer_topic)
    for message in consumer:
        received_time = time.time()
        msg = message.value
        msg_id = msg.get('id')
        
        with lock:
            if msg_id in sent_messages:
                send_time = sent_messages.pop(msg_id)
                response_time = received_time - send_time
                print(f"Response Time for ID {msg_id}: {response_time:.4f} seconds")

def main():
    try:
        bootstrap_servers = os.getenv('KAFKA_BROKER', 'kafka:9092')
        producer_topic = "test"
        consumer_topic = "inference_result"
        
        print(f"Using Kafka bootstrap servers: {bootstrap_servers}")

        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            security_protocol="PLAINTEXT",
            api_version_auto_timeout_ms=5000,
            request_timeout_ms=5000,
            max_block_ms=5000
        )
        print("Successfully connected to Kafka to topic ", producer.topic)

        data_file = '/app/data_file.pkl'
        print(f"Opening data file: {data_file}")
        with open(data_file, 'rb') as fo:
            pic_dict = pickle.load(fo, encoding='bytes')

        labels = pic_dict[b'labels']
        data = pic_dict[b'data']
        print(f"Loaded {len(data)} records")

        for index in range(len(data)):
            data_string = ",".join(str(x) for x in data[index])
            msg_id = str(uuid.uuid4())

            json_object = {
                "id": msg_id,
                "ground_truth": int(labels[index]),
                "data": data_string
            }

            send_time = time.time()
            with lock:
                sent_messages[msg_id] = send_time

            producer.send(producer_topic, json_object)
            producer.flush()
            print(f"Sent message {index+1}/{len(data)} with ID: {msg_id}")
            time.sleep(1)

        producer.close()
        print("Finished sending messages, waiting for processing...")

        timeout = 60
        start_time = time.time()
        while time.time() - start_time < timeout:
            with lock:
                if not sent_messages:
                    print("All messages processed successfully.")
                    break
            time.sleep(1)

    except Exception as e:
        print(f"Error in producer: {e}")

if __name__ == "__main__":
    main()