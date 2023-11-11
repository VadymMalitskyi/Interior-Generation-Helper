# Use an official CUDA runtime as a parent image
FROM mambaorg/micromamba:jammy-cuda-12.2.0
USER root

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    bzip2 \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /data
COPY data/ data/

WORKDIR /weights
COPY output_dir/L1F6VFKD0 weights/

WORKDIR /app
RUN git clone https://github.com/VadymMalitskyi/ATISS.git
WORKDIR /app/ATISS

# ENV PATH="/root/miniconda3/bin:${PATH}"
# ARG PATH="/root/miniconda3/bin:${PATH}"
# RUN wget \
#     https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
#     && mkdir /root/.conda \
#     && bash Miniconda3-latest-Linux-x86_64.sh -b \
#     && rm -f Miniconda3-latest-Linux-x86_64.sh 

# RUN conda env create -y -f environment.yaml && \
#     conda activate interior-gen-helper && \
#     cd ATISS && \
#     python setup.py build_ext --inplace && \
#     pip install -e . && \
#     cd ..

