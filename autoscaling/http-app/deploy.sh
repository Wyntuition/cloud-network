IMAGE=http-app:latest

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

# test connectivty to the service
kubectl run -it --rm debug --image=busybox -- nslookup http-app

# Watch pod metrics every 2 seconds (w/cpu %)
watch -n 2 "kubectl top pods"
watch -n 2 'kubectl top pods --use-protocol-buffers | awk '\''{if(NR>1)printf "%s: CPU %d%%\n",$1,($2*100)/200}'\'''

# Watch deployment replicas
watch -n 2 "kubectl get deployment http-app"
# Watch HPA status
watch -n 2 "kubectl get hpa"
# Watch pods with labels
watch -n 2 "kubectl get pods -l app=http-app"

###################### Monitoring HPA ######################
# Combined view (horizontal scaling + CPU usage, and node metrics)
watch -n 2 'echo "=== PODS ==="; kubectl get pods -l app=http-app -o wide; echo "\n=== HPA ==="; kubectl get hpa; echo "\n=== CPU & Memory USAGE (PODS) ==="; kubectl top pods -l app=http-app; echo "\n=== NODE CPU & MEMORY USAGE ==="; kubectl top nodes'
# CPU and memory usage for pods
watch -n 2 'kubectl top pods --use-protocol-buffers | awk '\''{if(NR>1)printf "%s: CPU %.1f%%, Mem %.1f%%\n", $1, ($2*100)/2000, ($3*100)/1024}'\'''


# Request limits for VPA
kubectl get pods -l app=http-app -o jsonpath='{range .items[*]}{.metadata.name}{" - CPU: "}{.spec.containers[0].resources.requests.cpu}{" Memory: "}{.spec.containers[0].resources.requests.memory}{"\n"}{end}'
# Watch cpu and memory percentage
watch -n 2 'kubectl top pods --use-protocol-buffers | awk '\''{if(NR>1)printf "%s: CPU %.1f%%, Memory %.1f%%\n", $1, ($2*100)/2000, ($3*100)/1024}'\'''
