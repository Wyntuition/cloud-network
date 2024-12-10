docker build -t load-tester .
docker tag load-tester:latest localhost:5000/load-tester:latest
docker push localhost:5000/load-tester:latest
