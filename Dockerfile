FROM python:3.10.14-slim

# Python settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies (cached layer)
COPY requirements.txt .

RUN pip install --no-cache-dir uv && \
    uv venv /opt/venv && \
    uv pip install -r requirements.txt --python /opt/venv/bin/python && \
    rm -rf /root/.cache

# Use virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]