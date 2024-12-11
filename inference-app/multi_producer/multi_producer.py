import os
import time
from kafka import KafkaProducer
import sys
import json
import uuid
import threading
import pickle
import csv

KAFKA_BROKER = "192.168.5.15:9092"
TOPIC = "test"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    acks=1,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_messages(file_name, producer_id, results_file):
    with open(file_name, 'rb') as fo:
        pic_dict = pickle.load(fo, encoding='bytes')

    labels = pic_dict[b'labels']
    data = pic_dict[b'data']
    filenames = pic_dict[b'filenames']

    print(f"Producer {producer_id}: pushing {len(data)} records")

    with open(results_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for index in range(len(data)):
            data_string = ",".join(str(x) for x in data[index])
            json_object = {
                "id": str(uuid.uuid4()),
                "ground_truth": labels[index],
                "data": data_string
            }
            start_time = time.time()  # Record start time
            producer.send(TOPIC, json_object)
            producer.flush()
            end_time = time.time()  # Record end time
            duration = end_time - start_time  # Calculate time taken
            writer.writerow([producer_id, json_object['id'], duration])
            print(f"Producer {producer_id}: Sent message with ID: {json_object['id']} in {duration:.4f} seconds")

if __name__ == "__main__":
    file_name = sys.argv[1]
    num_producers = int(sys.argv[2])  # Number of producer
    results_file = sys.argv[3]  # Output file for results

    with open(results_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ProducerID', 'MessageID', 'Duration'])

    threads = []
    for i in range(num_producers):
        thread = threading.Thread(target=send_messages, args=(file_name, i+1, results_file))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    producer.close()
    print("All producers finished sending messages.")

