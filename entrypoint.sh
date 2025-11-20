#!/bin/bash

echo "Waiting for PostgreSQL..."

# Wait for PostgreSQL to be ready
while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser if none exists
echo "Creating superuser..."
python manage.py create_superuser_if_none_exists

# Collect static files (if needed)
# python manage.py collectstatic --noinput

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
