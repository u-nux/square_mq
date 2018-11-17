#!/bin/bash

docker pull mongo
docker stop project-square-mongo
docker rm project-square-mongo

docker pull rabbitmq:management
docker stop project-square-rabbitmq
docker rm project-square-rabbitmq

docker build -t project-square .
docker stop project-square
docker rm project-square

docker run -d --name project-square-rabbitmq --hostname my-rabbit -p 15672:15672 rabbitmq:management
docker run -d --name project-square-mongo -v /home/yunus/mongodir:/data/db mongo

sleep 60

docker run -d --name project-square -p 5000:5000 --link project-square-rabbitmq:rabbit --link project-square-mongo:mongo project-square