#!/bin/bash
DOCKER_BUILDKIT=0 docker-compose up -d --build -t 10000
docker-compose restart