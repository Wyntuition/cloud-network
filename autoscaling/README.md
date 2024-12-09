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
