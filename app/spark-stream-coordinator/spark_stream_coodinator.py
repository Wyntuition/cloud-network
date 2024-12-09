from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, when, count
from pyspark.sql.types import StructType, StringType, IntegerType

# Kafka and MongoDB configurations
KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "test"
MONGO_URI = "mongodb://mongodb:27017/"
DATABASE = "team5_vm3_db"
COLLECTION = "incorrect_inference_results"

# Define the schema of the incoming Kafka messages
schema = StructType([
    ("id", StringType()),
    ("image_prediction", StringType()),
    ("actual_value", StringType()),
    ("producer_id", IntegerType())
])

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Stream Incorrect Inference Analysis") \
    .config("spark.mongodb.output.uri", f"{MONGO_URI}{DATABASE}.{COLLECTION}") \
    .getOrCreate()

# Read streaming data from Kafka
df_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# Deserialize Kafka messages and extract data
df_parsed = df_stream.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Add a column to identify incorrect predictions
df_with_flag = df_parsed.withColumn(
    "is_incorrect",
    when(col("image_prediction") != col("actual_value"), 1).otherwise(0)
)

# Perform aggregation to count incorrect inferences per producer
result_df = df_with_flag.groupBy("producer_id") \
    .agg(count(when(col("is_incorrect") == 1, True)).alias("incorrect_count"))

# Write the streaming results to MongoDB
result_stream = result_df.writeStream \
    .format("mongo") \
    .outputMode("complete") \
    .option("checkpointLocation", "/tmp/spark_checkpoints") \
    .option("uri", f"{MONGO_URI}{DATABASE}.{COLLECTION}") \
    .start()

# Wait for the termination of the streaming job
result_stream.awaitTermination()
