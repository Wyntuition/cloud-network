import json
from kafka import KafkaConsumer
import pymongo
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('pymongo').setLevel(logging.WARNING)  # Suppress pymongo debug logs

KAFKA_BROKER = '192.168.5.221:9092'
RESULTS_TOPIC = 'ml_predictions'
MONGO_URI = 'mongodb://192.168.5.143:27017/'  # Replace with your MongoDB URI

def connect_to_kafka(broker_address, topic):
    """Connect to Kafka and subscribe to a topic."""
    try:
        logger.info("Connecting to Kafka broker...")
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=broker_address,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='db_consumer_group_new',
            auto_offset_reset='latest'
        )
        logger.info(f"Connected to Kafka broker and subscribed to topic: {topic}")
        return consumer
    except Exception as e:
        logger.error(f"Error connecting to Kafka broker: {e}")
        raise

def connect_to_mongo(uri):
    """Connect to MongoDB and return the database collection."""
    try:
        logger.info("Connecting to MongoDB...")
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Trigger exception if connection fails
        logger.info("Connected to MongoDB successfully!")
        return client["team5_vm3_db"]["images"]
    except ServerSelectionTimeoutError as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise

def process_message(msg, collection):
    """Process a single Kafka message and insert into MongoDB."""
    try:
        data = msg.value
        msg_id = data['id']
        inferred_value = data.get('InferredValue')

        if inferred_value is None:
            logger.error(f"No 'InferredValue' in message ID {msg_id}")
            return

        # Update or insert the document in MongoDB
        result = collection.update_one(
            {'id': msg_id},
            {'$set': {'InferredValue': inferred_value}},
            upsert=True
        )

        if result.matched_count > 0:
            logger.info(f"Updated existing document with ID: {msg_id}")
        elif result.upserted_id is not None:
            logger.info(f"Inserted new document with ID: {msg_id}")
        else:
            logger.info(f"No changes made to document with ID: {msg_id}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")

def main():
        consumer = None
        try:
            consumer = connect_to_kafka(KAFKA_BROKER, RESULTS_TOPIC)
            collection = connect_to_mongo(MONGO_URI)

            logger.info("Listening for messages...")
            for msg in consumer:
                process_message(msg, collection)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:
            if consumer:
                consumer.close()
                logger.info("Kafka consumer closed.")

if __name__ == "__main__":
    main()

