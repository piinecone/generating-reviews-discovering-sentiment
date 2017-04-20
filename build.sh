#!/bin/bash

BACKEND=$1
IMAGE=sentiment-neuron
if [ -z ${BACKEND} ]; then 
    echo "Setting backend: CPU [default]"
    docker build -t $IMAGE -f Dockerfile.gpu .
else
    echo "Setting backend: GPU/NVIDIA"
    docker build -t $IMAGE -f Dockerfile .
fi