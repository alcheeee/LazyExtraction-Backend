#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD="${DATABASE_PASSWORD}" psql -h "${DATABASE_HOST}" -U "${DATABASE_USER}" -d "${DATABASE_NAME}" -c '\q'; do
  echo "PostgreSQL is still unavailable - sleeping"
  sleep 3
done

echo "Running Alembic Migrations"
alembic upgrade head

echo "Starting FastAPI application"
exec uvicorn app.main:app --host ${FASTAPI_HOST} --port ${FASTAPI_PORT} --workers 7 --reload