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
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
        
        logger.info(f"Connecting to Kafka at {kafka_bootstrap_servers}")
        consumer = KafkaConsumer(
            'test',
            bootstrap_servers=kafka_bootstrap_servers,
            auto_offset_reset='earliest',
            group_id='consumer_group',
            value_deserializer=lambda x: x.decode('utf-8')
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
                json_object["inferedValue"] = ""
                msg_id = json_object['id']
                
                mycol.insert_one(json_object)
                logger.info(f"Inserted message with ID: {msg_id}")
                
                retrieved_document = mycol.find_one({"id": msg_id})
                if retrieved_document: 
                    logger.info(f"Verified document: {retrieved_document['id']}")
                else:
                    logger.warning(f"Document not found after insertion: {msg_id}")
                    
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    except Exception as e:
        logger.error(f"Fatal error in consumer: {e}")
    finally:
        consumer.close()
        logger.info("Consumer service stopped")

if __name__ == "__main__":
    main()