# Set up a local registry to use with the Kubernetes cluster
docker run -d --name kind-registry --restart=always -p 5000:5000 registry:2
curl http://localhost:5000/v2/_catalog

# Create a Kind cluster using the configuration
kind create cluster --name kind-autoscaling-test --config=kind-config.yaml
kubectl cluster-info --context kind-autoscaling-test
# Connect the registry container to the Kind network
docker network connect "kind" kind-registry
docker exec -it kind-control-plane crictl info | grep "localhost:5000"

