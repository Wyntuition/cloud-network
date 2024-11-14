#!/bin/bash

registry_url="192.168.5.15:5000"

# For each subdirectory, go in and run docker tag and docker push using the registry_url
for dir in */; do
    if [ -d "$dir" ]; then
        # Remove the trailing slash from the directory name
        image_name="${dir%/}"
        echo "Processing image: $image_name"
        sudo docker build -t "$image_name" "$dir"
        sudo docker tag "$image_name" "$registry_url/$image_name"
        sudo docker push "$registry_url/$image_name"
    fi
doneps 