# Cloud network

Code used in going deep in cloud computing per a graduate school class, including standing up VM networks, a Kubernetes cluster, and native Kubernetes autoscaling experiments.

- [autoscaling/](autoscaling/README.md) - experiments with autoscaling in Kubernetes
- [VM network via Ansible](vm-network-ansible/README.md) - set up multiple VMs networked together to learn IaC via Ansible
- [Kubernetes Ansible playbooks](kubernetes-playbooks/) - Stand up a Kubernetes cluster on the VM network using Ansible
- [Inference App](inference-app/) - multi-microservice-based application with heavy communication and coordination, for doing ML image recognition, as a good test app

## VM network for Cloud Computing

## Running

1. On `vm1`
	1. Run Zookeeper with `./run-zookeeper`, then run Kafka broker with `./run-kafka`
	1. Run `python3 producer.py`
1. On `v3`, ensure Mongo started
`. On 'vm4', ensure ml model and endpoint is started
1. On `vm2`
	1. Run `python3 db_consumer.py`
	1. Run `python3 inference_consumer.py`

Architecture:
vm1 - IoT, Broker, Producer
vm2 - Db Consumer - done; Inference consumer - Not Done
vm3 - Mongodb - done
vm4 - ML - half done.. need to consumer to send data to ML and then connect to MongoDb to send updated inferred value


