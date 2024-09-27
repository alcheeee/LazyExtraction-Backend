#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD="${DB_PASSWORD}" psql -h "${DB_HOST}" -U "${DB_USER}" -d "${DB_NAME}" -c '\q'; do
  echo "PostgreSQL is still unavailable - sleeping"
  sleep 3
done

echo "Running Alembic Migrations"
alembic upgrade head

echo "Starting FastAPI application"
exec uvicorn app.run:server --host ${FASTAPI_HOST} --port ${FASTAPI_PORT} --workers 7 --reload
