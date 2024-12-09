IMAGE=http-app:latest

docker build -t http-app .

kubectl create deployment http-app --image=$IMAGE
kubectl expose deployment http-app --type=LoadBalancer --port=8080



# Apply HPA
kubectl autoscale deployment http-app --cpu-percent=50 --min=1 --max=10

# Load testing
k6 run -u 50 -d 1m script.js # Simulate 50 users for 1 minute

# Monitor scaling events
kubectl get hpa http-app -w

# Metrics collection for scaling and resource use
kubectl top pods
kubectl top nodes
