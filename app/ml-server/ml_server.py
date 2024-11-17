from kafka import KafkaConsumer, KafkaProducer
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import json
import logging
from logging.config import dictConfig

# Configure Logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
})

logger = logging.getLogger(__name__)

# Load the pre-trained ResNet50 model
try:
    logger.info("Loading ResNet50 model...")
    model = ResNet50(weights='imagenet')
    logger.info("ResNet50 model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load ResNet50 model: {e}")
    model = None

# Kafka configuration
KAFKA_BROKER = 'kafka:9092'
INPUT_TOPIC = 'test'
OUTPUT_TOPIC = 'ml_predictions'

# Setup Kafka consumer
try:
    consumer = KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='ml_server_group_new',
        auto_offset_reset='latest',
        max_partition_fetch_bytes=10485760,
        fetch_max_bytes=52428800
    )
    logger.info(f"Kafka consumer connected and subscribed to topic '{INPUT_TOPIC}'.")
except Exception as e:
    logger.error(f"Failed to connect Kafka consumer: {e}")
    consumer = None

# Setup Kafka producer
try:
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        max_request_size=10485760
    )
    logger.info("Kafka producer connected and ready.")
except Exception as e:
    logger.error(f"Failed to connect Kafka producer: {e}")
    producer = None

def process_image(image_data):
    try:
        # Convert the comma-separated string back to a NumPy array
        image_array = np.fromstring(image_data, sep=',', dtype=np.uint8)
        image_array = image_array.reshape((32, 32, 3))  # Adjust dimensions as needed

        # Resize to 224x224 as required by ResNet50
        img = image.array_to_img(image_array)
        img = img.resize((224, 224))

        # Preprocess the image
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Make prediction
        preds = model.predict(x)
        decoded_preds = decode_predictions(preds, top=1)
        prediction = decoded_preds[0][0][1]  # Get the predicted class label

        return prediction
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return None

def main():
    if consumer is None:
        logger.error("Kafka consumer is not available. Exiting.")
        return

    logger.info("Starting message consumption.")
    for message in consumer:
        try:
            data = message.value
            if data is None:
                logger.error("Received None data, possibly due to deserialization failure.")
                continue

            logger.debug(f"Received message: {data}")

            if not isinstance(data, dict):
                logger.error(f"Expected message value to be a dict, got {type(data)} instead.")
                continue

            image_data = data.get('data')
            message_id = data.get('id', 'Unknown')

            if not image_data:
                logger.error(f"No 'data' field found in message ID {message_id}.")
                continue

            logger.info(f"Processing image for message ID {message_id}.")
            prediction = process_image(image_data)

            if prediction is None:
                logger.error(f"Invalid image data for message ID {message_id}.")
                continue

            output = {
                'id': message_id,
                'InferredValue': prediction
            }

            if producer:
                producer.send(OUTPUT_TOPIC, output)
                producer.flush()
                logger.info(f"Processed image ID {message_id}, prediction: {prediction}")
            else:
                logger.error("Kafka producer is not available. Cannot send output.")

        except Exception as e:
            logger.error(f"Error processing message: {e}")

if __name__ == "__main__":
    main()

