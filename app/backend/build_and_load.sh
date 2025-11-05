#!/bin/sh
#build and load image into kind
# ./build_and_load.sh <image tag> 


if [$# -eq 0 ]; then
  echo "Useage: $0 <image tag>"
  exit 1
else 
    docker build . -t weather_api:v$1
    sudo kind load docker-image weather_api:v$1 --name weather-app
fi
