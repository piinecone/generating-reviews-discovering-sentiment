#!/bin/bash

IMAGE=sentiment-neuron
docker build -t $IMAGE -f Dockerfile .