from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count

# MongoDB connection details
MONGO_URI = "mongodb://mongodb:27017/"
DATABASE = "team5_vm3_db"
COLLECTION = "images"

# Initialize Spark session with MongoDB connector
spark = SparkSession.builder \
    .appName("Incorrect Inference Analysis") \
    .config("spark.mongodb.input.uri", f"{MONGO_URI}{DATABASE}.{COLLECTION}") \
    .getOrCreate()

# Load data from MongoDB
df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

# Select relevant columns and calculate mismatch
df_filtered = df.select("image_prediction", "actual_value", "producer_id") \
    .withColumn("is_incorrect", when(col("image_prediction") != col("actual_value"), 1).otherwise(0))

# Perform aggregation to count incorrect inferences per producer
result_df = df_filtered.groupBy("producer_id") \
    .agg(count(when(col("is_incorrect") == 1, True)).alias("incorrect_count"))

# Show the results
result_df.show()

# Save the results (optional) to MongoDB or another collection
result_df.write.format("mongo") \
    .mode("overwrite") \
    .option("uri", f"{MONGO_URI}{DATABASE}.incorrect_inference_results") \
    .save()

# Stop Spark session
spark.stop()
