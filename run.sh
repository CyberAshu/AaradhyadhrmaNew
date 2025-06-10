#!/usr/bin/env bash
# Exit on error
set -o errexit

# Run database migrations
python manage.py migrate

# Create superuser if not exists (temporary workaround for Render)
# Replace 'admin', 'admin@aaradhyadhrma.com' with desired credentials
# Remove or comment out this section after initial setup for security
if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(is_superuser=True).exists() else 1)"; then
    echo "Creating superuser..."
    # Use environment variable for password to avoid hardcoding
    if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
        python manage.py createsuperuser --noinput --username admin --email admin@aaradhyadhrma.com --password $DJANGO_SUPERUSER_PASSWORD || echo 'Superuser creation failed or already exists.'
        echo "Superuser created successfully with provided password."
    else
        echo "DJANGO_SUPERUSER_PASSWORD environment variable not set. Superuser creation will fail without password."
        python manage.py createsuperuser --noinput --username admin --email admin@aaradhyadhrma.com || echo 'Superuser creation failed or already exists.'
    fi
    echo "Please ensure DJANGO_SUPERUSER_PASSWORD is set in Render environment variables for secure password setup."
fi

# Start the Gunicorn server
gunicorn aaradhyadhrma.wsgi:application --bind 0.0.0.0:$PORT