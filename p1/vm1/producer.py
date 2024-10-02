import os   # need this for popen
import time # for sleep
from kafka import KafkaProducer  # producer of events
import sys
import matplotlib.pyplot as plt
import cv2
import pickle
import json
import uuid
import numpy as np


producer = KafkaProducer (bootstrap_servers="192.168.5.221:9092", 
                                          acks=1,
                                          value_serializer=lambda v: json.dumps(v).encode('utf-8')) 

file_name = sys.argv[1]
with open(file_name, 'rb') as fo:
    pic_dict = pickle.load(fo ,encoding='bytes')

labels = pic_dict[b'labels']
data = pic_dict[b'data']
filenames = pic_dict[b'filenames']

print("pushing: ", len(data), " records") 

for index in range(len(data)):
    data_string = ",".join(str(x) for x in data[index])

    json_object = {
        "id": str(uuid.uuid4()),
        "ground_truth": labels[index],
        "data": data_string
    }

    # Send the json_object directly without serializing again
    producer.send("test", json_object)
    producer.flush()
    print(f"Sent message with ID: {json_object['id']}")

producer.close() 

