# selecting a base docker container with cuda and cudnn installed that maches the VM used to build the docker
FROM python:3.10

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# setting up the environment 

# not sure if the base docker is regularly updated so adding the essential 
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    unzip \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

# I prefer having the model and code downloaded in the docker if the model and the code version is not changing
# but to be able to use CD we should pull the code everytime and download the model
WORKDIR /code

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/code"

# upgrade and install the requirements
RUN pip3 install --no-cache-dir -Ur requirements.txt

# Envioronment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Expose a port to recieve requests
EXPOSE 80

# Start the app, the prediction is being made in GPU and its using an instance with one GPU only
CMD ["gunicorn", "-b", "0.0.0.0:80", "inference.app:app", "--workers", "1", "-k", "uvicorn.workers.UvicornWorker"]

# To handle in multiple requests I hosted the ECR in ECS using fargate