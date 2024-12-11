# Add --from-beginning flag to see all messages
#sudo kubectl exec -it kafka-client -- kafka-console-consumer --bootstrap-server kafka:9092 --topic test --from-beginning

# Send message
#sudo kubectl exec kafka-client -- kafka-console-producer --broker-list kafka:9092 --topic test < test_message.txt

# List topics and partitions
sudo kubectl exec -it kafka-client -- kafka-topics --bootstrap-server kafka:9092 --describe --topic test

# Describe topic & see metadata like broker
sudo kubectl exec -it kafka-client -- kafka-topics --describe --topic test --bootstrap-server kafka:9092


# Check consumer groups
sudo kubectl exec -it kafka-client -- kafka-consumer-groups --bootstrap-server kafka:9092 --list

# Check consumer group offsets
sudo kubectl exec -it kafka-client -- kafka-consumer-groups --bootstrap-server kafka:9092 --describe --group <group-id>

# Broker id and leader
 sudo kubectl exec -it kafka-client -- zookeeper-shell zookeeper:2181 ls /brokers/
ids

