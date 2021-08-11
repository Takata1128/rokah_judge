#!/bin/sh

# docker stop $(docker ps -q)
# docker rm $(docker ps -q -a)
# docker rmi $(docker images -q) -f

# rsync -av app Dockerfiles/
docker-compose up -d --build