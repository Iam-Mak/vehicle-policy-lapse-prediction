FROM python:3.10.14-slim

# Python settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY services/model_service/requirements.txt .

RUN pip install --no-cache-dir uv && \
    uv venv /opt/venv && \
    uv pip install \
    --python /opt/venv/bin/python \
    -r requirements.txt && \
    rm -rf /root/.cache

# Use virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy full project
COPY . /app

# Create non-root user
RUN useradd --system --create-home appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose FastAPI port
EXPOSE 8001

# Run FastAPI application
CMD ["uvicorn","services.model_service.app:app", "--host", "0.0.0.0", "--port", "8001"]