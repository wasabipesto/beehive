#!/bin/bash
# builds a container with all dev project requirements
# launches it with full acess to the project files and an open port

docker build -t beehive-dev -f docker/Dockerfile . || exit
docker run -v /opt/beehive:/opt/beehive -p 3000:3000 -it --name beehive-dev beehive-dev
