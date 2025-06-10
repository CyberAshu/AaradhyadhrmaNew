#!/usr/bin/env bash
# Exit on error
set -o errexit

gunicorn aaradhyadhrma.wsgi:application --bind 0.0.0.0:$PORT