# PA 4

## Sumamry

We updated our app to send the inference messages with the producer id, installed Spark on our Kubernetes cluster, then updated our Python to count the incorrect inferences using a batch job out of the mongo data. 

Then, as extra, we attempted to stream Kafka directly to Spark and process that way.

Primary Data Source: team5_vm3_db.images

    This is where Kafka messages are initially inserted by your consumer application.
    Schema fields coming from Kafka: id, image_prediction, actual_value, producer_id.

Results Storage: team5_vm3_db.incorrect_inference_results

    This is a new MongoDB collection where the results of our incorrect inference calculations (aggregated data) are stored.


1. **Initial Schema in the `images` collection**:
   - When the Kafka consumer inserts messages into MongoDB, they have a structure like:
     ```json
     {
       "id": "some-id",
       "image_prediction": "value_a",
       "actual_value": "value_b",
       "producer_id": 123
     }
     ```

2. **Processing Schema Changes**:
   - We calculate if the prediction is incorrect (where `image_prediction != actual_value`) using a derived column (`is_incorrect`) added during Spark's transformation logic.

3. **Result Schema for `incorrect_inference_results`**:
   - Group by `producer_id`.
   - Count mismatches (`is_incorrect`) for each producer.
   - Example schema structure in `incorrect_inference_results`:
     ```json
     {
       "producer_id": 123,
       "incorrect_count": 5
     }
     ```

---

### Summary of Flow
| Stage               | MongoDB Collection              | Schema Changes |
|---------------------|----------------------------------|----------------|
| Kafka Consumer writes raw messages into MongoDB (`team5_vm3_db.images`). | `team5_vm3_db.images` | `{"id", "image_prediction", "actual_value", "producer_id"}` |
| Spark Structured Streaming processes data (calculates `is_incorrect` and aggregates by `producer_id`). | Processed in-memory DataFrame | Aggregates errors and counts by producer_id |
| Results are saved to MongoDB `incorrect_inference_results`. | `team5_vm3_db.incorrect_inference_results` | `{"producer_id": int, "incorrect_count": int}` |


## Code & Results

Spark is now installed in our Kubernetes cluster via Helm. 

### Batch job

The code for batch processing the mongo inference data via Spark, is in `app/spark-consumer/spark_batch_consumer.py`


```

```

Results of inaccurate count, written to Mongo:
```

```



### Stream job

We have another python script that connects Spark directly to Kakfa in `app/spark-consumer/spark_stream_consumer.py`


Messages from Kafka from the inference engine, saved in Mongo streamed from Kafka into Spark:
```
{
  "id": "12345",
  "image_prediction": "cat",
  "actual_value": "dog",
  "producer_id": 101
}
...

## Documentation of effort

- A lot of Kubernetes learning still, in scaling properly
- Spark learning - docs, how to install it on Kubernetes, how to use it in Python
- How to do batch processing with Spark
- How to do stream processing directly against Kafka

## Work split

Run the job again with a large amount of data
Record which producer is sending messages
Install spark
Use spark in Python to process the results in the DB, to calculate incorrect inferences by producer
Save output to csv and graph





