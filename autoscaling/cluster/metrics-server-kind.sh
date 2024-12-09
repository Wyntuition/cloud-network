# Add metrics-server helm repo
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm repo update

# Install metrics-server with Kind-specific values
helm install metrics-server metrics-server/metrics-server \
  --namespace kube-system \
  --set args="{--kubelet-insecure-tls=true,--kubelet-preferred-address-types=InternalIP}" \
  --set hostNetwork.enabled=true

# Verify installation
kubectl get pods -n kube-system -l k8s-app=metrics-server
kubectl top nodes
kubectl get deployment metrics-server -n kube-system
