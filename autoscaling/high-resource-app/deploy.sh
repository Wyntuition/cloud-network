docker build -t high-resource-app .
docker tag high-resource-app:latest localhost:5000/high-resource-app:latest
docker push localhost:5000/high-resource-app:latest
curl http://localhost:5000/v2/_catalog


kubectl apply -f high-resource-app.yaml
