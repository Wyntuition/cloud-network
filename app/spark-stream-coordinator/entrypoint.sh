#!/bin/bash
# Ensure Spark processes run correctly
echo "Starting Spark Streaming Application..."
exec spark-submit --master k8s://https://kubernetes.default.svc.cluster.local:6443 \
  --deploy-mode cluster \
  --name stream_coordinator \
  --class main /app/spark_stream_coordinator.py "$@"
