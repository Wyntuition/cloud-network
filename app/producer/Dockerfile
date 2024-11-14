FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the default command
CMD ["python", "producer.py"]
