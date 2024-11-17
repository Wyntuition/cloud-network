
cd producer
sudo docker build -t producer . 
sudo docker tag producer 192.168.5.169:5000/producer
sudo docker push  192.168.5.169:5000/producer

cd  ../consumer
sudo docker build -t consumer . 
sudo docker tag consumer 192.168.5.169:5000/consumer
sudo docker push  192.168.5.169:5000/consumer

CD ../ml-server
sudo docker build -t ml-server .
sudo docker tag ml-server 192.168.5.169:5000/ml-server
sudo docker push  192.168.5.169:5000/ml-server
