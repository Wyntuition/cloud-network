#!/bin/bash

echo "Starting simulated batch processing from MongoDB..."

# Simulate MongoDB-like data by creating a list of fake documents
FAKE_DATA=(
  '{"producer_id": "0", "image_prediction": "2", "actual_value": "3"}'
  '{"producer_id": "0", "image_prediction": "4", "actual_value": "4"}'
  '{"producer_id": "0", "image_prediction": "5", "actual_value": "5"}'
  '{"producer_id": "1", "image_prediction": "7", "actual_value": "3"}'
  '{"producer_id": "1", "image_prediction": "5", "actual_value": "8"}'
  '{"producer_id": "1", "image_prediction": "8", "actual_value": "2"}'
  '{"producer_id": "2", "image_prediction": "9", "actual_value": "5"}'
  '{"producer_id": "2", "image_prediction": "1", "actual_value": "1"}'
  '{"producer_id": "2", "image_prediction": "4", "actual_value": "6"}'
  '{"producer_id": "3", "image_prediction": "4", "actual_value": "6"}'
  '{"producer_id": "3", "image_prediction": "2", "actual_value": "3"}'
  '{"producer_id": "3", "image_prediction": "8", "actual_value": "8"}'
  '{"producer_id": "4", "image_prediction": "6", "actual_value": "6"}'
  '{"producer_id": "4", "image_prediction": "9", "actual_value": "7"}'
  '{"producer_id": "4", "image_prediction": "0", "actual_value": "4"}'
  '{"producer_id": "5", "image_prediction": "5", "actual_value": "3"}'
  '{"producer_id": "5", "image_prediction": "1", "actual_value": "0"}'
  '{"producer_id": "5", "image_prediction": "3", "actual_value": "3"}'
  '{"producer_id": "6", "image_prediction": "4", "actual_value": "4"}'
  '{"producer_id": "6", "image_prediction": "7", "actual_value": "7"}'
  '{"producer_id": "6", "image_prediction": "2", "actual_value": "8"}'
  '{"producer_id": "7", "image_prediction": "3", "actual_value": "1"}'
  '{"producer_id": "7", "image_prediction": "0", "actual_value": "0"}'
  '{"producer_id": "7", "image_prediction": "6", "actual_value": "2"}'
  '{"producer_id": "8", "image_prediction": "5", "actual_value": "5"}'
  '{"producer_id": "8", "image_prediction": "1", "actual_value": "0"}'
  '{"producer_id": "8", "image_prediction": "8", "actual_value": "6"}'
  '{"producer_id": "9", "image_prediction": "7", "actual_value": "4"}'
  '{"producer_id": "9", "image_prediction": "9", "actual_value": "9"}'
  '{"producer_id": "9", "image_prediction": "2", "actual_value": "5"}'
  '{"producer_id": "10", "image_prediction": "4", "actual_value": "7"}'
  '{"producer_id": "10", "image_prediction": "0", "actual_value": "0"}'
  '{"producer_id": "10", "image_prediction": "3", "actual_value": "4"}'
  '{"producer_id": "11", "image_prediction": "3", "actual_value": "8"}'
  '{"producer_id": "11", "image_prediction": "2", "actual_value": "2"}'
  '{"producer_id": "11", "image_prediction": "7", "actual_value": "0"}'
  '{"producer_id": "12", "image_prediction": "5", "actual_value": "2"}'
  '{"producer_id": "12", "image_prediction": "0", "actual_value": "1"}'
  '{"producer_id": "12", "image_prediction": "4", "actual_value": "3"}'
  '{"producer_id": "13", "image_prediction": "2", "actual_value": "2"}'
  '{"producer_id": "13", "image_prediction": "5", "actual_value": "8"}'
  '{"producer_id": "13", "image_prediction": "8", "actual_value": "0"}'
  '{"producer_id": "14", "image_prediction": "7", "actual_value": "7"}'
  '{"producer_id": "14", "image_prediction": "1", "actual_value": "3"}'
  '{"producer_id": "14", "image_prediction": "3", "actual_value": "0"}'
  '{"producer_id": "15", "image_prediction": "0", "actual_value": "2"}'
  '{"producer_id": "15", "image_prediction": "2", "actual_value": "5"}'
  '{"producer_id": "15", "image_prediction": "6", "actual_value": "6"}'
  '{"producer_id": "16", "image_prediction": "1", "actual_value": "1"}'
  '{"producer_id": "16", "image_prediction": "4", "actual_value": "8"}'
  '{"producer_id": "16", "image_prediction": "3", "actual_value": "7"}'
  '{"producer_id": "17", "image_prediction": "0", "actual_value": "1"}'
  '{"producer_id": "17", "image_prediction": "3", "actual_value": "0"}'
  '{"producer_id": "17", "image_prediction": "5", "actual_value": "4"}'
  '{"producer_id": "18", "image_prediction": "2", "actual_value": "2"}'
  '{"producer_id": "18", "image_prediction": "6", "actual_value": "9"}'
  '{"producer_id": "18", "image_prediction": "9", "actual_value": "6"}'
  '{"producer_id": "19", "image_prediction": "4", "actual_value": "5"}'
  '{"producer_id": "19", "image_prediction": "1", "actual_value": "4"}'
  '{"producer_id": "19", "image_prediction": "8", "actual_value": "9"}'
)


# Simulate batch processing logic by counting incorrect inferences
declare -A counts

echo "Processing simulated data..."
for doc in "${FAKE_DATA[@]}"; do
  # Parse JSON fields using jq-like logic simulation
  producer_id=$(echo "$doc" | grep -oP '"producer_id": "\K\d+"')
  image_prediction=$(echo "$doc" | grep -oP '"image_prediction": "\K\d+"')
  actual_value=$(echo "$doc" | grep -oP '"actual_value": "\K\d+"')

  # Compare values to simulate logic (image_prediction != actual_value)
  if [ "$image_prediction" != "$actual_value" ]; then
    counts["$producer_id"]=$((counts["$producer_id"] + 1))
  fi
done

# Print aggregated results
echo "Incorrect inference counts by producer_id:"
for key in "${!counts[@]}"; do
  echo "Producer ID: $key, Incorrect Inferences: ${counts[$key]}"
done

echo "Batch processing simulation complete."
