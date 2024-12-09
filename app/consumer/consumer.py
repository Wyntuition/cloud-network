import os
import time
from kafka import KafkaConsumer
import json 
import pymongo 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting consumer service...")
        
        kafka_bootstrap_servers = os.getenv('KAFKA_BROKER', 'kafka:9092')
        session_timeout_ms = int(os.getenv('SESSION_TIMEOUT_MS', '30000'))
        heartbeat_interval_ms = int(os.getenv('HEARTBEAT_INTERVAL_MS', '10000'))
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
        
        logger.info(f"Connecting to Kafka at {kafka_bootstrap_servers}")
        consumer = KafkaConsumer(
            'test',
            bootstrap_servers=kafka_bootstrap_servers,
            auto_offset_reset='earliest',
            group_id='consumer_group',
            value_deserializer=lambda x: x.decode('utf-8'),
            session_timeout_ms=session_timeout_ms,
            heartbeat_interval_ms=heartbeat_interval_ms
        )
        
        logger.info("Successfully connected to Kafka")

        logger.info(f"Connecting to MongoDB at {mongo_uri}")
        myclient = pymongo.MongoClient(mongo_uri)
        myclient.server_info()
        mydb = myclient["team5_vm3_db"]
        mycol = mydb["images"]
        logger.info("Successfully connected to MongoDB")

        logger.info("Starting message processing loop...")
        for msg in consumer:
            try:
                json_object = json.loads(msg.value)
                
                # Ensure 'inferedValue' is added
                json_object["inferedValue"] = ""
                
                msg_id = json_object.get('id', 'unknown_id')
                producer_id = json_object.get('producer_id', 'unknown_producer')
                
                # Prepare document for MongoDB
                document = {
                    "id": msg_id,
                    "producer_id": producer_id,
                    "ground_truth": json_object.get('ground_truth', None),
                    "data": json_object.get('data', ''),
                    "inferedValue": json_object["inferedValue"]
                }
                
                # Insert into MongoDB
                mycol.insert_one(document)
                logger.info(f"Inserted message with ID: {msg_id} from Producer: {producer_id}")
                
                # Optional: Verify insertion
                retrieved_document = mycol.find_one({"id": msg_id})
                if retrieved_document:
                    logger.info(f"Verified document: ID={retrieved_document['id']}, Producer={retrieved_document['producer_id']}")
                else:
                    logger.warning(f"Document not found after insertion: ID={msg_id}")
                    
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    except Exception as e:
        logger.error(f"Fatal error in consumer: {e}")
    finally:
        if 'consumer' in locals():
            consumer.close()
            logger.info("Consumer service stopped")

if __name__ == "__main__":
    main()
