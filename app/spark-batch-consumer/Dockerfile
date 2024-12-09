# Use the official Spark image with Python support as a base
FROM bitnami/spark:3.2.1-scala2.12-python3

# Set environment variables for Spark
ENV SPARK_MODE=driver \
    PYSPARK_PYTHON=python3 \
    SPARK_HOME=/opt/spark

# Install MongoDB Python driver and other required Python dependencies
RUN pip install pymongo pandas

# Copy the batch processing script into the container
COPY spark_batch_consumer.py /app/spark_batch_consumer.py

# Set the working directory
WORKDIR /app

# Run the script (you can pass arguments here if needed)
CMD ["python", "spark_batch_consumer.py"]
