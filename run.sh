#!/usr/bin/env bash
# Exit on error
set -o errexit

# Run database migrations
python manage.py migrate

# Start the Gunicorn server
gunicorn aaradhyadhrma.wsgi:application --bind 0.0.0.0:$PORT