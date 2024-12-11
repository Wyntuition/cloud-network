docker build -t metrics-viewer .
docker tag metrics-viewer:latest localhost:5000/metrics-viewer:latest
docker push localhost:5000/metrics-viewer:latest

kubectl apply -f deploy.yaml