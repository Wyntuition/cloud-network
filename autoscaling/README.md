# Analysis of Native Autoscaling in Kubernetes

Overview:
- Running scenarios for HPA and VPA:
    - Stand up app that can take HTTP requests
    - Simulate variable request loads to endpoint with a load tester
    - Simulate raising memory usage in pod
- Observe effects:
    - See how Kubernetes increases and decreases the number of pods, 
    - Timing and windows 
    - Nodes placed on
    - CPU and memory use on the pods and nodes
    - Seeing how Kubernetes changing the pod's resource limits, and changes resourse usage, noticing timing and winodws, nodes placed on, memory usage on the pod and nodes
- Recording metrics: CPU and memory use on pods and across cluster, request rate, endpoint latency, data processed

HPA vs VPA:

```mermaid
graph TD
    A[Scaling Strategies] --> B[VPA: Vertical Scaling]
    A --> C[HPA: Horizontal Scaling]
    
    B --> D[Increases Pod Resources]
    B --> E[Single Pod Gets More CPU/Memory]
    
    C --> F[Adds More Pod Replicas]
    C --> G[Distributes Load Across Pods]
```

## Test Environment

We are using a Kubernetes cluster, developed locally with Kind, and using VMs on Chameleon for scaling up. 


### HPA load testing architecture 

```mermaid
flowchart TB
    subgraph Load Tester Pods
        LT1[Load Tester Pod 1<br>50-100 users<br>Multiple workers]
        LT2[Load Tester Pod 2<br>50-100 users<br>Multiple workers]
        LT3[Load Tester Pod 3<br>50-100 users<br>Multiple workers]
    end

    subgraph App Pods
        AP1[App Pod 1]
        AP2[App Pod 2]
        AP3[App Pod 3]
    end

    KS[Kubernetes Service]
    HPA[Horizontal Pod Autoscaler<br>Scale threshold: CPU > 50%]

    LT1 --> KS
    LT2 --> KS
    LT3 --> KS

    KS --> AP1
    KS --> AP2
    KS --> AP3

    HPA --> AP1
    HPA --> AP2
    HPA --> AP3

    style LT1 fill:#f96,stroke:#333,stroke-width:2px
    style LT2 fill:#f96,stroke:#333,stroke-width:2px
    style LT3 fill:#f96,stroke:#333,stroke-width:2px
    style AP1 fill:#77dd77,stroke:#333,stroke-width:2px
    style AP2 fill:#77dd77,stroke:#333,stroke-width:2px
    style AP3 fill:#77dd77,stroke:#333,stroke-width:2px
    style KS fill:#4287f5,stroke:#333,stroke-width:2px
    style HPA fill:#ff6b6b,stroke:#333,stroke-width:2px
```


## Observability

- Dashboard of pods on each node used to observe real time behavior: 
https://github.com/learnk8s/k8bit




## To do:

Horizontal Pod Autoscaling scenarios:
1. Set up HTTP-based app so we can load test endpoint and see Kubernetes horizontally scale the pod by increasing and decreasing the number of pods based on load
1. Set up load tester to send request loads: small (to get it to scale down), medium, large (to get it to scale up)
1. Observe and record metrics of resource use in pod and across cluster, how pod count changes and when, request rate and latency as a result

Vertical Pod Autoscaling scenarios:
1. Set up app that requires a lot of resources in the pod, that will need more, setting resource limit
1. Set up load tester/test script to increase the resource use in the pod, making Kubernetes raise the resource limit
1. Observe and record metrics of resource use in pod and across cluster, how the limits change when, data processing rate as a result


## Steps

1. Install Kubernetes cluster (Kind for local, then via Ansible for real nodes)
1. Configure node capacity 
1. Install Kubernetes Metrics Server so things like node and pod resource usage can be gathered with kubectl

HPA
1. Set resource requests and limits for deployment/pod
1. Create HPA on deployment with min/max pods
1. Run `polinux/stress` to [spike CPU to limit in Kubernetes](high-resource-app/stress.yaml)
1. View activity with `kubectl top pods -A`. 
1. View limits on node with `kubectl describe nodes` and:
    ```
    kubectl get nodes -o json | jq '.items[] | {name: .metadata.name, capacity: .status.capacity, allocatable: .status.allocatable}'
    ```
1. Test scenarios:
    - Scale out
    - Scale down
    - Rapid spike in load
    - Gradual increase in load
      Different scraping limits
      Different metrics used
1. Show prometheus and grafana
    - Total requests
    - Request duration
    - Requests per second: `rate(http_requests_total[1m])`
1. Max requests it can get to, and how fast. Tweaks if needed faster. 

## Observations

- 1 pod at 1 pod at 500m CPU and 25Mi Memory.  1 load tester (~200-800 RPS).
    - Requests being sent: 
    - Requests per second:
        - Average 380
        - Peak  758
        - Median 636
    - CPU usage:
        - Average 485m (24.7%)
    - Memory usage:
        - Average: 28Mi (2.3%)
- 2 pods, 10 load testers
    - Requests per second:
        - Average 436
        - Peak  3241
        - Median 711


![Alt text](graph-hpa.png "Effect of HPA")

## Conclusions

Increasing the  number of pods is appropriate when:
- The application can scale horizontally (e.g., stateless apps).
- Requests are distributed across multiple instances.
- Resource limits for a single pod would be exceeded by the load.
- The application is resilient to distributed state.
- Examples:
    - Microservices with variable load
    - Web applications
    - Background processing systems
    - API endpoints

Increasing the resources of a pod is appropriate when:
- The application is stateful or cannot scale horizontally
- The pod's workload is growing, but the number of requests is stable
- Kubernetes detects that resource requests are insufficient for the workload
- Plan fopr cooldown periods to prevent thrashing
- Consider scaling delays
- Configure appropriate thresholds
- Consider potential scaling latency
- Metrics consideration - scarping frequency, accuracy

```mermaid
flowchart TD
    subgraph k8s_cluster["Kubernetes Cluster"]
        subgraph http_app_service["HTTP App Service"]
            service["Service"]
        end

        subgraph http_app_pods["HTTP Application Pods"]
            http_app_1["HTTP App Pod 1"]
            http_app_2["HTTP App Pod 2"]
            http_app_3["HTTP App Pod 3"]
            http_app_4["HTTP App Pod 4"]
        end

        subgraph load_tester_pods["Load Tester Pods"]
            lt_pod_1["Load Tester Pod 1"]
            lt_pod_2["Load Tester Pod 2"]
            lt_pod_3["Load Tester Pod 3"]
            lt_pod_4["Load Tester Pod 4"]
            lt_pod_5["Load Tester Pod 5"]
            
            lt_worker_1["Worker 1 (Simulates 50-100 users)"]
            lt_worker_2["Worker 2 (Simulates 50-100 users)"]
            lt_worker_3["Worker 3 (Simulates 50-100 users)"]
            lt_worker_4["Worker 4 (Simulates 50-100 users)"]
            lt_worker_5["Worker 5 (Simulates 50-100 users)"]
            
            lt_pod_1 --> lt_worker_1
            lt_pod_2 --> lt_worker_2
            lt_pod_3 --> lt_worker_3
            lt_pod_4 --> lt_worker_4
            lt_pod_5 --> lt_worker_5
        end

        subgraph hpa["Horizontal Pod Autoscaler"]
            hpa_manager["HPA Manager"]
            hpa_manager -.-> http_app_pods
        end

        subgraph metrics["/metrics scraping"]
            prometheus_scraper["Prometheus Scraper"]
            prometheus_db["Prometheus DB"]
        end
    end

    %% Connections
    lt_worker_1 -.-> service
    lt_worker_2 -.-> service
    lt_worker_3 -.-> service
    lt_worker_4 -.-> service
    lt_worker_5 -.-> service

    service --> http_app_1
    service --> http_app_2
    service --> http_app_3
    service --> http_app_4

    http_app_1 --> prometheus_scraper
    http_app_2 --> prometheus_scraper
    http_app_3 --> prometheus_scraper
    http_app_4 --> prometheus_scraper

    prometheus_scraper --> prometheus_db
    prometheus_db -.-> metrics

    hpa_manager -.-> http_app_1
    hpa_manager -.-> http_app_2
    hpa_manager -.-> http_app_3
    hpa_manager -.-> http_app_4

    %% HPA Logic
    classDef hpaLogic fill:#f9f,stroke:#333,stroke-width:2px;
    hpa_manager:::hpaLogic
```

### Metrics collection archtecture

Here are some diagrams to show how our http-app uses the Prometheus libs to expose metrics at /metrics for Prometheus to scrape them. The endpoint will contain metrics like `http_requests_total` and `http_request_duration_seconds`. It does this via a ServiceMonitor object which Prometheus installed in Kubernetes added. Then Grafana queries Prometheus' database to pull and visualize the data.

```mermaid
flowchart TD
    subgraph http_app ["HTTP Application"]
        http_server[HTTP Server on :8080]
        metrics_endpoint["/metrics endpoint"]
        handler_function["Handler Function"]
        prometheus_client["Prometheus Metrics Library"]
        
        http_server --> handler_function
        handler_function --> prometheus_client
        prometheus_client --> metrics_endpoint
    end

    subgraph prometheus["Prometheus Server"]
        prometheus_scraper["Scraper"]
        prometheus_db["Metrics DB"]
        
        prometheus_scraper --> prometheus_db
    end

    subgraph grafana["Grafana"]
        grafana_ui["Grafana UI"]
        grafana_db["Prometheus DB"]
        
        grafana_ui --> grafana_db
    end

    %% Connections
    http_app --> prometheus
    prometheus --> grafana
    metrics_endpoint --> prometheus_scraper
    prometheus_db --> grafana_db
```

```mermaid
flowchart TD
    subgraph k8s_cluster ["Kubernetes Cluster"]
        subgraph app_pods["HTTP Application Pods"]
            http_pod_1["HTTP App Pod 1"]
            http_pod_2["HTTP App Pod 2"]
            metrics_endpoint["/metrics endpoint"]
            cpu_usage["CPU Usage Metric"]
            memory_usage["Memory Usage Metric"]
            request_time["Request Time Metric"]
            
            http_pod_1 --> metrics_endpoint
            http_pod_2 --> metrics_endpoint
            metrics_endpoint --> cpu_usage
            metrics_endpoint --> memory_usage
            metrics_endpoint --> request_time
        end

        subgraph service_monitor["Service Monitor"]
            service_monitor_obj["ServiceMonitor"]
            service_monitor_obj --> app_pods
        end

        prometheus_scraper["Prometheus Scraper"]
    end

    subgraph prometheus["Prometheus"]
        prometheus_db["Prometheus DB"]
        prometheus_scraper --> prometheus_db
    end

    subgraph grafana["Grafana"]
        grafana_ui["Grafana UI"]
        grafana_db["Prometheus DB"]
        
        grafana_ui --> grafana_db
    end

    %% Connections
    service_monitor_obj --> prometheus_scraper
    prometheus_scraper --> prometheus_db
    prometheus_db --> grafana_db
    grafana_db --> grafana_ui
```

**Expected requests per second (RPS) based on different CPU and memory limits for a typical Go web application:**

| CPU Limit | Memory Limit | Expected RPS Range | Typical Use Case | Performance Characteristics |
|-----------|--------------|-------------------|-----------------|----------------------------|
| 100m      | 128Mi        | 50-150 RPS        | Small microservice, lightweight API | Low traffic, dev/staging |
| 250m      | 256Mi        | 150-300 RPS       | Medium complexity service | Moderate web application |
| 500m      | 512Mi        | 300-500 RPS       | High-traffic service | Production web API |
| 1000m (1 core) | 1Gi     | 500-1000 RPS      | Heavy traffic service | High-performance API |
| 2000m (2 cores) | 2Gi     | 1000-2000 RPS     | Enterprise-level service | Mission-critical application |


**Typical CPU Limit Ranges**

| Application Type         | CPU Request (Minimum) | CPU Limit (Maximum) |
|--------------------------|-----------------------|---------------------|
| Static file servers      | 50m                  | 200m                |
| Lightweight REST APIs    | 100m                 | 500m                |
| Medium-complexity APIs   | 200m                 | 1 CPU               |
| High-complexity APIs     | 500m                 | 2-4 CPU             |
| Heavy computational apps | 1 CPU                | 4+ CPU              |

---

### Best Practices
1. Start Small and Scale:
   - Start with conservative limits, e.g., `100m` request and `500m` limit.
   - Monitor performance (latency, CPU usage) under typical and peak traffic.
1. Enable horizontal autoscaling and configure/tune properly
1. Load test
1. Monitor and adjust

### Key Considerations:
  1. Application complexity
  2. Database interactions
  3. External service calls
  4. Concurrency design
  5. Network latency
  6. Specific business logic

### Example Decision Flow
1. Start with a baseline: `200m` request and `1 CPU` limit.
2. Monitor:
   - Is the average CPU usage consistently above 80% of the limit? **Increase the limit.**
   - Is the CPU usage far below the request? **Lower the request or limit.**
3. Test with a real-world traffic simulation.
4. Enable autoscaling if traffic patterns vary significantly. 