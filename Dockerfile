FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
LABEL maintainer="me@kanade.org"

RUN apt update && apt upgrade -y && apt install -y --no-install-recommends \
    python3-dev \
    python3-pip \
    ffmpeg \
    git \
    git-lfs

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY main.py main.py
RUN git clone https://huggingface.co/Salesforce/blip-image-captioning-base
ENV HF_DATASETS_OFFLINE=1
ENV TRANSFORMERS_OFFLINE=1
CMD ["python3","./main.py"]
EXPOSE 5000
