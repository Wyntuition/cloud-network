#!/bin/bash

# Function to get version for a command
get_version() {
    local command=$1
    if command -v $command &> /dev/null; then
        echo "$command version:"
        $command version --short
    else
        echo "$command is not installed"
    fi
}

# Get versions for kubeadm, kubelet, and kubectl
get_version kubeadm
get_version kubelet
get_version kubectl

# Get the version of the Kubernetes API server from the kubelet
if command -v kubelet &> /dev/null; then
    echo "Kubelet version information (with API server details):"
    kubelet --version
else
    echo "Kubelet is not installed"
fi

# Fetch the Kubernetes API version (requires kubeadm)
if command -v kubeadm &> /dev/null; then
    echo "Kubernetes API Server version info from kubeadm:"
    kubeadm version
else
    echo "kubeadm is not installed"
fi

# Get the versions of any related Kubernetes services or tools
# For example, you could check for containerd version (used by Kubernetes)
if command -v containerd &> /dev/null; then
    echo "Containerd version:"
    containerd --version
else
    echo "Containerd is not installed"
fi

# Check Docker version if using Docker as the container runtime
if command -v docker &> /dev/null; then
    echo "Docker version:"
    docker --version
else
    echo "Docker is not installed"
fi
