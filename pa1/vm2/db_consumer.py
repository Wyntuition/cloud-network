import os
import time
from kafka import KafkaConsumer  # KafkaError removed
import json
import pymongo
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError

KAFKA_BROKER = '192.168.5.221:9092'
RESULTS_TOPIC = 'ml_predictions'
MONGO_URI = 'mongodb://192.168.5.143:27017/'

def connect_to_kafka(broker_address, topic):
    """Connect to Kafka and subscribe to a topic."""
    try:
        print("Connecting to Kafka broker...")
        consumer = KafkaConsumer(bootstrap_servers=broker_address)
        consumer.subscribe([topic])
        print(f"Connected to Kafka broker and subscribed to topic: {topic}")
        return consumer
    except Exception as e:  # Generic Exception used here
        print(f"Error connecting to Kafka broker: {e}")
        raise

def connect_to_mongo(uri):
    """Connect to MongoDB and return the database collection."""
    try:
        print("Connecting to MongoDB...")
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Trigger exception if connection fails
        print("Connected to MongoDB successfully!")
        return client["team5_vm3_db"]["images"]
    except ServerSelectionTimeoutError as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

def process_message(msg, collection):
    """Process a single Kafka message and insert into MongoDB."""
    try:
        json_string = str(msg.value, 'ascii')
        json_object = json.loads(json_string)
        json_object2dict = eval(json_object)  # This could be simplified, eval is risky
        json_object2dict["inferedValue"] = ""

        msg_id = json_object2dict['id']

        # Insert into MongoDB
        insert_result = collection.insert_one(json_object2dict)
        print(f"Inserted document with ID: {msg_id}")

        # Verify document insertion
        retrieved_document = collection.find_one({"id": msg_id})
        if retrieved_document:
            print(f"Verified inserted document with ID: {retrieved_document['id']}")
        else:
            print(f"Document not found after insertion!")
    except (json.JSONDecodeError, KeyError, PyMongoError) as e:
        print(f"Error processing message: {e}")

def main():
    consumer = None
    try:
        consumer = connect_to_kafka(KAFKA_BROKER, RESULTS_TOPIC)
        collection = connect_to_mongo(MONGO_URI)

        print("Listening for messages...")
        for msg in consumer:
            process_message(msg, collection)

    except Exception as e:  # Catch all errors here
        print(f"An error occurred: {e}")
    finally:
        if consumer:
            consumer.close()
            print("Kafka consumer closed.")

if __name__ == "__main__":
    main()
