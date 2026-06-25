#!/bin/bash

set -e

ACR_NAME="vehiclelapseacr12345.azurecr.io"

echo "Logging into Azure Container Registry..."
az acr login --name $ACR_NAME

echo "Building model-service..."
docker build \
  --platform linux/amd64 \
  -t model-service:v1 \
  -f services/model_service/Dockerfile .

echo "Tagging model-service..."
docker tag \
  model-service:v1 \
  $ACR_NAME/model-service:v1

echo "Pushing model-service..."
docker push \
  $ACR_NAME/model-service:v1

echo "Building api-gateway..."
docker build \
  --platform linux/amd64 \
  -t api-gateway:v1 \
  -f services/api_gateway/Dockerfile .

echo "Tagging api-gateway..."
docker tag \
  api-gateway:v1 \
  $ACR_NAME/api-gateway:v1

echo "Pushing api-gateway..."
docker push \
  $ACR_NAME/api-gateway:v1

echo "Done!"