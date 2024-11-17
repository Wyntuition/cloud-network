import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
import json 
import pymongo 

# Get Kafka and MongoDB configuration from environment variables
kafka_bootstrap_servers = os.getenv('KAFKA_BROKER', 'kafka:9092')
kafka_topic = os.getenv('KAFKA_TOPIC', 'test')
mongodb_connection_string = os.getenv('MONGODB_CONNECTION_STRING', 'mongodb://mongodb:27017/')
mongodb_database = os.getenv('MONGODB_DATABASE', 'team5_vm3_db')
mongodb_collection = os.getenv('MONGODB_COLLECTION', 'images')
print(f"v0.1 Kafka Broker: {kafka_bootstrap_servers}")
print(f"Kafka Topic: {kafka_topic}")
print(f"MongoDB Connection String: {mongodb_connection_string}")
print(f"MongoDB Database: {mongodb_database}")
print(f"MongoDB Collection: {mongodb_collection}")

# consumer = KafkaConsumer (bootstrap_servers="192.168.5.221:9092")
kafka_bootstrap_servers = os.getenv('KAFKA_BROKER', 'kafka:9092')

# consumer.subscribe (topics=["test"])
# Initialize Kafka Consumer with exception handling
try:
    consumer = KafkaConsumer(
        kafka_topic,
        bootstrap_servers=kafka_bootstrap_servers
    )
    print(f"Connected to Kafka broker at {kafka_bootstrap_servers}")
except KafkaError as e:
    print(f"Failed to connect to Kafka broker at {kafka_bootstrap_servers}: {e}")
    consumer = None

# myclient = pymongo.MongoClient("mongodb://mongodb:27017/")
# myclient.server_info()
# Initialize MongoDB Client with exception handling
try:
    myclient = pymongo.MongoClient(mongodb_connection_string)
    myclient.server_info()  # Trigger a connection to check if MongoDB is reachable
    print(f"Connected to MongoDB at {mongodb_connection_string}")
except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB at {mongodb_connection_string}: {e}")
    myclient = None


if consumer and myclient:
    print("Successfully connected to Kafka and MongoDB. Ready to consume messages.")
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
        
else:
    print("Kafka consumer or MongoDB client not initialized. Keeping the pod running for inspection.")
    while True:
        time.sleep(60)  # Sleep to keep the pod running





