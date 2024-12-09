spark-submit \
    --master k8s://https://192.168.5.15 \
    --deploy-mode cluster \
    --conf spark.kubernetes.container.image=192.168.5.169:5000/spark-batch:latest \
    --class org.apache.spark.deploy.PythonRunner \
    local:///path/to/your/script.py
