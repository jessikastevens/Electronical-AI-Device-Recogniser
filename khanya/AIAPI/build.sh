#!/bin/bash

VERSION_FILE="version.txt"
SERVICE=collyer-khanya-prediction-svc
PROJECTID=collyers-435813
REPOID=collyers-main
REGION=europe-west2

source ./function.sh
builder_checker
version_increase

docker buildx build --push --tag $REGION-docker.pkg.dev/$PROJECTID/$REPOID/$SERVICE:latest --tag $REGION-docker.pkg.dev/$PROJECTID/$REPOID/$SERVICE:$VERSION --platform linux/amd64 .