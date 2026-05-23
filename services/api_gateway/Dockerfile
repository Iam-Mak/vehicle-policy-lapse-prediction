FROM python:3.10.14-slim

# Python settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Set working directory
WORKDIR /app

# Install dependencies
COPY services/api_gateway/requirements.txt .

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

# Expose Flask port
EXPOSE 5000

# Run Flask with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "services.api_gateway.app:app"]