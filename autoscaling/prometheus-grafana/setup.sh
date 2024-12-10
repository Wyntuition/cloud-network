# helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
# helm install prometheus prometheus-community/prometheus

# # Install Prometheus with default configurations
# helm install prometheus-stack prometheus-community/kube-prometheus-stack \
#   --namespace monitoring --create-namespace

# # helm install grafana bitnami/grafana
# helm install grafana prometheus-community/grafana \
#   --namespace monitoring



helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://charts.helm.sh/stable
helm repo update

kubectl create namespace monitoring

helm install kind-prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --set prometheus.service.nodePort=30000 --set prometheus.service.type=NodePort --set grafana.service.nodePort=31000 --set grafana.service.type=NodePort --set alertmanager.service.nodePort=32000 --set alertmanager.service.type=NodePort --set prometheus-node-exporter.service.nodePort=32001 --set prometheus-node-exporter.service.type=NodePort
kubectl --namespace monitoring get pods -l release=kind-prometheus

