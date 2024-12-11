# helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
# helm repo update
helm install my-release oci://registry-1.docker.io/bitnamicharts/spark

# Install Spark operator
helm install spark-operator spark-operator/spark-operator --namespace spark-operator --create-namespace

# Verify operator is running
kubectl get pods -n spark-operator

