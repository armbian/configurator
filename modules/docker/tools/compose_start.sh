#!/bin/sh

# Only accept one argument :
# 1: Path to the compose file

docker-compose -f "${1}" up -d
