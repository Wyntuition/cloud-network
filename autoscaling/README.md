# Analysis of Native Autoscaling in Kubernetes

Overview:
- Running scenarios for HPA and VPA:
    - Simulate variable request loads to endpoint
    - Simulate raising memory usage in pod
- Observing behavior of pods
    - See how Kubernetes increases and decreases the number of pods, noticing timing and windows, nodes placed on, CPU and memory use on the pods and nodes
    - Seeing how Kubernetes changing the pod's resource limits, and changes resourse usage, noticing timing and winodws, nodes placed on, memory usage on the pod and nodes
- Recording metrics: CPU and memory use on pods and across cluster, request rate, endpoint latency, data processed

## Test Environment

We are using a Kubernetes cluster, developed locally with Kind, and using VMs on Chameleon for scaling up. 

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




## Conclusions

Increasing the  number of pods is appropriate when:
- The application can scale horizontally (e.g., stateless apps).
- Requests are distributed across multiple instances.
- Resource limits for a single pod would be exceeded by the load.
- The application is resilient to distributed state.

Increasing the resources of a pod is appropriate when:
- The application is stateful or cannot scale horizontally
- The pod's workload is growing, but the number of requests is stable
- Kubernetes detects that resource requests are insufficient for the workload

Plan fopr cooldown periods to prevent thrashing

