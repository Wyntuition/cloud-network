docker build -t http-app .
docker tag http-app:latest localhost:5000/http-app:latest
docker push localhost:5000/http-app:latest
