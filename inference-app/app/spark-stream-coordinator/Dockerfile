# Base image with Python
FROM apache/spark-py:3.3.1

# Set environment variables to Spark defaults
ENV SPARK_HOME=/opt/spark \
    PATH=$SPARK_HOME/bin:$PATH \
    PYSPARK_PYTHON=python3

# Switch to root for package installation
USER root

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    && pip3 install --no-cache-dir pymongo kafka-python

# Copy Python scripts into the image
WORKDIR /app
COPY ./ /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]