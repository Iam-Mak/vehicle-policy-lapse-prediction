# Deployment

## Overview

The application is containerized using Docker to ensure a consistent runtime across development and deployment environments. The API is served using Gunicorn inside the container and deployed on Azure Web App.

## Setup

* Base image: `python:3.10-slim`
* Dependencies installed from `requirements.txt`
* Virtual environment created at `/opt/venv`
* Application served via Gunicorn

## Design Decisions

* **Slim base image**
  Reduces image size while maintaining compatibility with required libraries

* **Pinned dependencies**
  Ensures reproducibility across environments

* **Layer caching**
  `requirements.txt` copied before application code to speed up rebuilds

* **Non-root user**
  Improves container security

* **Environment configuration**
  Disabled bytecode generation and enabled unbuffered logging for cleaner runtime behavior

* **.dockerignore usage**
  Excludes unnecessary files to reduce image size

## Current Deployment

* Containerized using Docker
* Deployed on Azure Web App
* API served using Gunicorn

## Future Improvements

* Separate API and model service into independent containers
* Add health checks for service monitoring
* Introduce orchestration (e.g., Kubernetes)
* Add scaling and load balancing support
