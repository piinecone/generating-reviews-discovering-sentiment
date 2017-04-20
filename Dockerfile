#
# Sentiment Neuron Dockerfile (Tensorflow)
# Tensorflow + GPU
#
# @see https://hub.docker.com/r/tensorflow/tensorflow/tags/
#
FROM tensorflow/tensorflow:latest-py3

MAINTAINER Loreto Parisi loretoparisi@gmail.com

RUN pip install \
    numpy \
    tqdm \
    scipy \
    scikit-learn

WORKDIR /sentiment/

COPY ./ /sentiment/

CMD nvidia-smi -q
CMD ["bash"]