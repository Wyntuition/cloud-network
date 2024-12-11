import os
import time
from kafka import KafkaProducer, KafkaConsumer
import sys
import threading
import pickle
import json
import uuid
import numpy as np

# Shared data structure to keep track of message IDs and their send timestamps
sent_messages = {}

# Lock for thread-safe operations on the shared data structure
lock = threading.Lock()

def consumer_thread_function(bootstrap_servers, consumer_topic):
    consumer = KafkaConsumer(
        consumer_topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=str(uuid.uuid4()),  # Unique group ID to ensure the consumer reads all messages
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    for message in consumer:
        received_time = time.time()
        msg = message.value
        msg_id = msg.get('id')

        # Check if the message ID is in our sent messages
        with lock:
            if msg_id in sent_messages:
                send_time = sent_messages.pop(msg_id)
                response_time = received_time - send_time
                print(f"Received inference result for ID: {msg_id}, Response Time: {response_time:.4f} seconds")
            else:
                # Message not sent by this producer or already processed
                continue

def main():
    # Kafka configuration
    bootstrap_servers = os.getenv('KAKFA_BROKER', 'kafka:9092')
    producer_topic = "test"
    consumer_topic = "inference_result"

    print(f"v0.1 Using Kafka bootstrap servers: {bootstrap_servers}")

    # Initialize Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        acks=1,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # Start the consumer thread
    consumer_thread = threading.Thread(
        target=consumer_thread_function,
        args=(bootstrap_servers, consumer_topic),
        daemon=True  # Daemon thread will close when the main program exits
    )
    consumer_thread.start()

    # Load data
    file_name = sys.argv[1]
    with open(file_name, 'rb') as fo:
        pic_dict = pickle.load(fo, encoding='bytes')

    labels = pic_dict[b'labels']
    data = pic_dict[b'data']
    filenames = pic_dict[b'filenames']

    print("pushing:", len(data), "records")

    for index in range(len(data)):
        data_string = ",".join(str(x) for x in data[index])

        msg_id = str(uuid.uuid4())
        json_object = {
            "id": msg_id,
            "ground_truth": labels[index],
            "data": data_string
        }

        # Record the send time before sending the message
        send_time = time.time()
        with lock:
            sent_messages[msg_id] = send_time

        # Send the message
        producer.send(producer_topic, json_object)
        producer.flush()
        print(f"Sent message with ID: {msg_id}")

    producer.close()

    # Wait for all messages to be processed
    while True:
        with lock:
            if not sent_messages:
                print("All messages have been processed.")
                break
        time.sleep(1)

if __name__ == "__main__":
    main()
