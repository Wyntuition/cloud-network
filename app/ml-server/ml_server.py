import os
from kafka import KafkaConsumer, KafkaProducer
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import json
import logging
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s: %(message)s',
    }},
    'handlers': {'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
})

logger = logging.getLogger(__name__)

try:
    logger.info("Loading ResNet50 model...")
    model = ResNet50(weights='imagenet')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')
INPUT_TOPIC = 'test'
OUTPUT_TOPIC = 'inference_result'

try:
    consumer = KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        group_id='ml_server_group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    logger.info("Kafka connections established")
except Exception as e:
    logger.error(f"Kafka connection failed: {e}")
    consumer = None
    producer = None

def process_image(image_data):
    try:
        image_array = np.fromstring(image_data, sep=',', dtype=np.uint8)
        image_array = image_array.reshape((32, 32, 3))

        img = image.array_to_img(image_array)
        img = img.resize((224, 224))
        
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = model.predict(x)
        decoded_preds = decode_predictions(preds, top=1)
        prediction = decoded_preds[0][0][1]

        return prediction
    except Exception as e:
        logger.error(f"Image processing error: {e}")
        return None

def main():
    if not all([consumer, producer, model]):
        logger.error("Required components not available")
        return

    logger.info("Starting message processing")
    
    for message in consumer:
        try:
            data = message.value
            image_data = data.get('data')
            message_id = data.get('id')

            if not image_data:
                logger.error(f"No data in message {message_id}")
                continue

            prediction = process_image(image_data)
            if prediction:
                output = {
                    'id': message_id,
                    'prediction': prediction
                }
                producer.send(OUTPUT_TOPIC, output)
                producer.flush()
                logger.info(f"Processed message {message_id}")

        except Exception as e:
            logger.error(f"Processing error: {e}")

if __name__ == "__main__":
    main()
