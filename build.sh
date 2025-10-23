#!/usr/bin/env bash

if [ "$#" -lt 1 ]; then
  echo "Usage: ./build.sh ./imagedir/ [docker build args ...]"
  exit 1
fi

IMAGE_DIR="$1"
shift
BUILD_ARGS="$@"

if [ ! -e ${IMAGE_DIR}/Dockerfile ]; then
  echo "Cannot find ${IMAGE_DIR}/Dockerfile"
  exit 1
fi

IMAGE_NAME=$(basename ${IMAGE_DIR})
IMAGE_NAME="pauldmccarthy/${IMAGE_NAME}"
IMAGE_TAG="$(date +%Y%m%d).$(git describe --tags --always --dirty)"

docker buildx build               \
  ${BUILD_ARGS}                   \
  -t "${IMAGE_NAME}:${IMAGE_TAG}" \
  -t "${IMAGE_NAME}:latest"       \
  -f ${IMAGE_DIR}/Dockerfile      \
   ./resources/
