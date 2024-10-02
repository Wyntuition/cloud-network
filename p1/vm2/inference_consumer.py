import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
import json 
import pymongo 

consumer = KafkaConsumer (bootstrap_servers="192.168.5.221:9092")

consumer.subscribe (topics=["test"])


for msg in consumer:
    
    json_string = str(msg.value, 'ascii')

    json_object = json.loads(json_string)
    
    json_object2dict = eval(json_object)
    
    json_object2dict["inferedValue"] = ""

    msg_id = json_object2dict['id']

    # add code to send to ML
    # send json_object2dict[data] 
    # its an array of pixel values

consumer.close ()
    






