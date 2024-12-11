docker build -t spark-stream-coordinator .
docker tag spark-stream-coordinator 192.168.5.169:5000/spark-stream-coordinator:v0.5
docker push 192.168.5.169:5000/spark-stream-coordinator:v0.5
