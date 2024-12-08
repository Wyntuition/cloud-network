TAG=v0.2

echo "Building and pushing images to registry for tag: $TAG"

cd producer
sudo docker bq:quild -t producer . 
sudo docker tag producer 192.168.5.169:5000/producer:$TAG
sudo docker push  192.168.5.169:5000/producer:$TAG

cd  ../consumer
sudo docker build -t consumer . 
sudo docker tag consumer 192.168.5.169:5000/consumer:$TAG
sudo docker push  192.168.5.169:5000/consumer:$TAG

cd ../ml-server
sudo docker build -t ml-server .
sudo docker tag ml-server 192.168.5.169:5000/ml-server:$TAG
sudo docker push  192.168.5.169:5000/ml-server:$TAG
