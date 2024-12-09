# Add --from-beginning flag to see all messages
#sudo kubectl exec -it kafka-client -- kafka-console-consumer --bootstrap-server kafka:9092 --topic test --from-beginning

# List topics and partitions
sudo kubectl exec -it kafka-client -- kafka-topics --bootstrap-server kafka:9092 --describe --topic test

# Check consumer groups
sudo kubectl exec -it kafka-client -- kafka-consumer-groups --bootstrap-server kafka:9092 --list

# Check consumer group offsets
sudo kubectl exec -it kafka-client -- kafka-consumer-groups --bootstrap-server kafka:9092 --describe --group <group-id>
