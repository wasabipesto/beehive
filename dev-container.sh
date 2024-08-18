#!/bin/bash
# builds a container with all dev project requirements
# launches it with full acess to the project files and an open port

docker stop beehive-dev
docker rm beehive-dev
docker build -t beehive-dev -f docker/Dockerfile . || exit
docker run -it \
    -v /opt/beehive:/opt/beehive \
    -p 3000:3000 \
    --name beehive-dev \
    beehive-dev
