#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z ${DATABASE_HOST} ${DATABASE_PORT}; do
  sleep 0.1
done

echo "Running Alembic Migrations"
alembic upgrade head

echo "Starting FastAPI application"
exec uvicorn app.main:app --host ${FASTAPI_HOST} --port ${FASTAPI_PORT} --workers 7 --reload