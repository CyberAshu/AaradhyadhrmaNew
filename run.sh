#!/usr/bin/env bash
# Exit on error
set -o errexit

# Run database migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py createsu

# Run database migrations
python manage.py migrate

# Start the server with Gunicorn
venv/bin/gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 aaradhyadhrma.wsgi:application