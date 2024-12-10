# Set up a local registry to use with the Kubernetes cluster
docker run -d --name kind-registry --restart=always -p 5000:5000 registry:2
curl http://localhost:5000/v2/_catalog

# Create a Kind cluster using the configuration
kind create cluster --name autoscaling-test --config=kind-config.yaml
# Verify cluster creation and extra resource settings
kubectl cluster-info --context autoscaling-test
kubectl get nodes -o yaml | grep -A5 kubeletExtraArgs
#docker exec -it <worker-node-container-id> cat /var/lib/kubelet/config.yaml

# Connect the registry container to the Kind network
docker network connect "kind" kind-registry
docker exec -it kind-control-plane crictl info | grep "localhost:5000"

# Install metrics server
./metrics-server-kind.sh