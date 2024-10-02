import os
import time
import json
import uuid
import numpy as np
import cv2
from kafka import KafkaProducer
from tensorflow.keras.datasets import cifar10



# Load CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

def add_noise(image):
    """Add Gaussian blur to the image to simulate a noisy environment."""
    return cv2.GaussianBlur(image, (5, 5), 0)

def create_producer(bootstrap_servers):
    """Create a Kafka producer."""
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def on_success(record_metadata):
    """Callback for successful message delivery"""
    print(f"Message delivered to {record_metadata.topic} [{record_metadata.partition}] at offset {record_metadata.offset}")

def on_error(excp):
    """Callback for message delivery failure"""
    print(f"Failed to deliver message: {excp}")

def send_image(producer, topic):
    """Send a random image from CIFAR-10 dataset to Kafka."""
    idx = np.random.randint(0, len(x_train))
    image = x_train[idx]
    label = class_names[y_train[idx][0]]
    print(f"Sending image with label: {label}")
    
    # Add noise to the image
    noisy_image = add_noise(image)
    
    # Encode the image as JPEG
    _, buffer = cv2.imencode('.jpg', noisy_image)
    image_data = buffer.tobytes()
    
    # Create a message with a unique ID, ground truth label, and image data
    message = {
        'ID': str(uuid.uuid4()),
        'GroundTruth': label,
        'Data': image_data.hex()
    }
    
    # Send the message to the Kafka topic with callbacks for success and failure
    future = producer.send(topic, message)
    future.add_callback(on_success).add_errback(on_error)
    
    producer.flush()  # Force sending all messages

def main():
    # Create a Kafka producer
    producer = create_producer(bootstrap_servers='192.168.5.221:9092')
    topic = 'test'
    
    try:
        while True:
            # Send an image to the Kafka topic every 5 seconds
            send_image(producer, topic)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        # Close the producer
        producer.close()

if __name__ == "__main__":
    main()
