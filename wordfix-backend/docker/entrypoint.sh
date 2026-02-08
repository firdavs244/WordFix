#!/bin/bash
set -e

echo "Waiting for database..."
until python manage.py check --database default > /dev/null 2>&1; do
    echo "  DB not ready, retrying in 2s..."
    sleep 2
done
echo "Database is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

exec "$@"
