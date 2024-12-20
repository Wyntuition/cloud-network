## Commands 

ansible-playbook -i inventory.ini -e "@variables.yaml" playbook_step_by_step.yaml

ansible-playbook -i inventory.ini -e "@variables.yaml" playbook_delete_vms.yaml

Test connection to VMs:
```
ansible all -m ping
```

## Installing Kubernetes cluster with Ansible:

P3: 

We used ansible to create our Kubernetes cluster, in addition to the VMs. Here is the ansible code:
Prereqs: 
- install libs needed such as certificates to get kubernetes binaries and gpg, disable swap, 
- we install kubelet, kubectl and kubeadm
- hold versions at current, we download the k8s gpg key and use it to get the binaries from the apt repo

The kubernetes cluster installation can then proceed:
- We have a section that applies to both master and worker VMs - enable ipv4 
- Then we run the playbook against master, as we have specified master and worker notes in the inventory file. 
    - Initializing the kubernetes master node involves runnng kubeadm init with the cidr to use, and we put in some ansible conditions to ensure the version is where we want
    - We then set up a kube config file so we can run the kubectl command against the node and get cluster info
    - We set up a network plugin for the cluster
    - We then get the kubeadm admin join command, and register it in ansible so the worker steps can get it and join to the master in the cluster
- For each of the 3 workers, we then just have to have it run that join command, we has been stored in an ansible variable

Next, in order to deploy our service images into the cluster we have to create kubernetes manifests for each of them
- deployments, pods, jobs, kafka, mongo

Then, we push our images into a registry where kubernets can get them when installing into the cluster.

Then, we run the kubectl command to install these into the cluster.

We now have everything running which we can inpect. 

We can then capture graphs created from the activity. 