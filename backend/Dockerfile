FROM python:3.12.2-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y netcat-traditional postgresql-client && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
