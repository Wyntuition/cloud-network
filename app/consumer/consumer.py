import os
import time
import logging
from kafka import KafkaConsumer
import json
import pymongo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    consumer = None
    try:
        print("Starting consumer service...")
        
        kafka_bootstrap_servers = os.getenv('KAFKA_BROKER', 'kafka:9092')
        session_timeout_ms = int(os.getenv('SESSION_TIMEOUT_MS', '30000'))
        heartbeat_interval_ms = int(os.getenv('HEARTBEAT_INTERVAL_MS', '10000'))
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
        
        print(f"Connecting to Kafka at {kafka_bootstrap_servers}")
        consumer = KafkaConsumer(
            'test',
            bootstrap_servers=kafka_bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='simple_consumer',
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            security_protocol="PLAINTEXT"
            session_timeout_ms=session_timeout_ms,
            heartbeat_interval_ms=heartbeat_interval_ms
        )
        print("Successfully connected to Kafka")
        
        print(f"Connecting to MongoDB at {mongo_uri}")
        myclient = pymongo.MongoClient(mongo_uri)
        myclient.server_info()
        mydb = myclient["team5_vm3_db"]
        mycol = mydb["images"]
        print("Successfully connected to MongoDB")
        
        print("Starting message processing loop...")
        for msg in consumer:
            try:
                json_object = msg.value
                json_object["inferedValue"] = ""
                msg_id = json_object['id']
                
                mycol.insert_one(json_object)
                print(f"Processed message with ID: {msg_id}")
                    
            except Exception as e:
                print(f"Error processing message: {e}")
                continue
                
    except Exception as e:
        print(f"Fatal error in consumer: {e}")
    finally:
        if consumer:
            consumer.close()
            print("Consumer service stopped")

if __name__ == "__main__":
    main()     