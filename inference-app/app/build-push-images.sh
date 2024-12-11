TAG=v0.5

echo "Building and pushing images to registry for tag: $TAG"

cd spark-batch-consumer
sudo docker build -t spark-batch-consumer . 
sudo docker tag producer 192.168.5.169:5000/spark-batch-consumer:$TAG
sudo docker push  192.168.5.169:5000/spark-batch-consumer:$TAG

# cd spark-stream-coordinator
# sudo docker build -t spark-stream-coordinator . 
# sudo docker tag producer 192.168.5.169:5000/spark-stream-coordinator:$TAG
# sudo docker push  192.168.5.169:5000/spark-stream-coordinator:$TAG


# cd producer
# sudo docker build -t producer . 
# sudo docker tag producer 192.168.5.169:5000/producer:$TAG
# sudo docker push  192.168.5.169:5000/producer:$TAG

# cd  ../consumer
# sudo docker build -t consumer . 
# sudo docker tag consumer 192.168.5.169:5000/consumer:$TAG
# sudo docker push  192.168.5.169:5000/consumer:$TAG

#cd ../ml-server
#sudo docker build -t ml-server .
#sudo docker tag ml-server 192.168.5.169:5000/ml-server:$TAG
#sudo docker push  192.168.5.169:5000/ml-server:$TAG
