#!/bin/bash

echo "Starting Kafka streaming process..."

# Loop to simulate continuous streaming of messages
while true; do
  # Generate random values for simulation
  IMAGE_PREDICTION=$((RANDOM % 10))  # Random prediction
  ACTUAL_VALUE=$((RANDOM % 10))      # Random actual value
  PRODUCER_ID=$((RANDOM % 5))        # Random producer_id between 0-4
  IS_INCORRECT=$(( IMAGE_PREDICTION != ACTUAL_VALUE ))  # Simulate mismatch logic

  # Simulate a JSON message payload
  FAKE_MESSAGE=$(cat <<EOF
{
  "image_prediction": "$IMAGE_PREDICTION",
  "actual_value": "$ACTUAL_VALUE",
  "producer_id": "$PRODUCER_ID",
  "is_incorrect": "$IS_INCORRECT"
}
EOF
)

  # Simulate Kafka stream processing by printing the message
  echo "[Kafka Stream Message] $FAKE_MESSAGE"

  # Simulate MongoDB save logic by printing the transformation
  if [ "$IS_INCORRECT" -eq 1 ]; then
    echo "[MongoDB Save] Saving incorrect inference for producer_id $PRODUCER_ID with prediction: $IMAGE_PREDICTION, actual_value: $ACTUAL_VALUE"
  fi

  # Wait for a short interval to simulate streaming
  sleep 0.5
done
