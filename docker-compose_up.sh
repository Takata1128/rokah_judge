#!/bin/sh

# docker stop $(docker ps -q)
# docker rm $(docker ps -q -a)
# docker rmi $(docker images -q) -f

# rsync -av app Dockerfiles/
sudo rm -r judge/.gnupg
docker-compose up -d --build