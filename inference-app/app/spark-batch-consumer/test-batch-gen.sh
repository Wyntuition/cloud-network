#!/bin/bash

# Simulate a larger fake dataset with only 4 producers (producer_id 0, 1, 2, 3)
FAKE_DATA=()

for i in {1..1000}; do
  producer_id=$((RANDOM % 4))  # Random producer_id between 0 and 3
  image_prediction=$((RANDOM % 10))  # Random image prediction value between 0 and 9
  actual_value=$((RANDOM % 10))  # Random actual value between 0 and 9
  FAKE_DATA+=("{\"producer_id\": \"$producer_id\", \"image_prediction\": \"$image_prediction\", \"actual_value\": \"$actual_value\"}")
done

# Simulate output
for data in "${FAKE_DATA[@]}"; do
  echo "$data"
  sleep 0.01  # Introduce a slight delay between entries to mimic data flow
done
