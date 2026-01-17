FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir uv
RUN uv venv /opt/venv
RUN uv pip install -r requirements.txt --python /opt/venv/bin/python

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]