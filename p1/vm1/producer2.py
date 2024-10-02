from kafka import KafkaProducer
from kafka.errors import KafkaError
import sys
import pickle
import json
import uuid

producer = KafkaProducer(
    bootstrap_servers="192.168.5.221:9092",
    acks=1,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

file_name = sys.argv[1]
with open(file_name, 'rb') as fo:
    pic_dict = pickle.load(fo, encoding='bytes')

labels = pic_dict[b'labels']
data = pic_dict[b'data']
filenames = pic_dict[b'filenames']

print("Pushing:", len(data), "records")

for index in range(len(data)):
    data_string = ",".join(str(x) for x in data[index])

    json_object = {
        "id": str(uuid.uuid4()),
        "ground_truth": labels[index],
        "data": data_string
    }

    future = producer.send("test", json_object)

    try:
        record_metadata = future.get(timeout=10)
        print(f"Sent message with ID: {json_object['id']}, topic: {record_metadata.topic}, partition: {record_metadata.partition}, offset: {record_metadata.offset}")
    except KafkaError as e:
        print(f"Failed to send message: {e}")

producer.close()

