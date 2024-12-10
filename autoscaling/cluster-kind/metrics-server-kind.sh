# Add metrics-server helm repo
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm repo update

# Install metrics-server with different port
helm install metrics-server metrics-server/metrics-server \
  --namespace kube-system \
  --set args="{--kubelet-insecure-tls=true,--kubelet-preferred-address-types=InternalIP,--secure-port=10260}" \
  --set hostNetwork.enabled=true \
  --set containerPort=10260

# Verify installation
kubectl get pods -n kube-system -l k8s-app=metrics-server
kubectl top nodes
kubectl get deployment metrics-server -n kube-system
