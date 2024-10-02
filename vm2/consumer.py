import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
import json 
import pymongo 

consumer = KafkaConsumer (bootstrap_servers="192.168.5.221:9092")

consumer.subscribe (topics=["test"])

myclient = pymongo.MongoClient("mongodb://192.168.5.143:27017/")
myclient.server_info()


mydb = myclient["team5_vm3_db"]
mycol = mydb["images"]


for msg in consumer:
    
    json_string = str(msg.value, 'ascii')

    json_object = json.loads(json_string)
    
    json_object2dict = eval(json_object)
    
    json_object2dict["inferedValue"] = ""

    msg_id = json_object2dict['id']

    mycol.insert_one(json_object2dict)

    retrieved_document = mycol.find_one({"id": msg_id})
    if retrieved_document: 
        print("Inserted Document:", retrieved_document['id'])
    else:
        print("Not found!!")


consumer.close ()
    






