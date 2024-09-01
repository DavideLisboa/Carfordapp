#!/bin/sh

set -e

# Wait until PostgreSQL is available
until pg_isready -h db -p 5432; do
  echo "Waiting for database to be ready..."
  sleep 2
done

echo "Database is up - creating database if it doesn't exist"

# Set the password environment variable for `psql` command
export PGPASSWORD="password"

# Create the database if it doesn't exist
psql -h db -U user -d postgres -c "CREATE DATABASE carford;" || echo "Database already exists"

echo "Database is up and ready"
exec "$@"
