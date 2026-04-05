## Purpose of Using Docker

Docker is used in this project to ensure a consistent and reproducible runtime environment for the application. It eliminates issues related to dependency conflicts and differences between development and deployment environments.

By containerizing the application, the setup process becomes simpler and more reliable, enabling the application to run uniformly across different systems.

## Docker Design Overview

### Objective

The goal is to containerize a Flask-based machine learning API to ensure a consistent, reproducible, and production-ready deployment.

### What Was Implemented

* A Docker image was created for a Flask API serving ML predictions
* Dependencies were installed inside an isolated virtual environment
* The application is served using Gunicorn
* A non-root user is used for security
* A `.dockerignore` file is used to reduce image size


### Key Design Decisions

#### 1. Base Image

* Used `python:3.10-slim`
* Reason: lightweight, stable, and compatible with ML libraries

#### 2. Dependency Management

* Used `requirements.txt` with pinned versions
* Installed dependencies inside a virtual environment (`/opt/venv`)
* Reason: ensures reproducibility and avoids system-level conflicts

#### 3. Layer Optimization

* Copied `requirements.txt` before application code
* Reason: enables Docker layer caching and faster rebuilds

#### 4. Environment Variables

* Disabled bytecode generation and enabled unbuffered logging
* Reason: cleaner filesystem and real-time logs in container

#### 5. Security

* Created and used a non-root user (`appuser`)
* Reason: reduces risk in case of vulnerabilities

#### 6. Application Execution

* Used Gunicorn as the production server
* Reason: better performance and concurrency than Flask dev server

#### 7. Image Optimization

* Used `.dockerignore` to exclude unnecessary files
* Reason: reduces image size and improves build efficiency


### Future Improvements

* Split into multiple services (API + model service)
* Add health checks for monitoring
* Introduce container orchestration (Kubernetes)
* Implement load balancing for scaling

---
---
