#!/usr/bin/env bash
# Exit on error
set -o errexit

# Run database migrations
python manage.py migrate

# Create or update superuser password (temporary workaround for Render)
# Replace 'admin', 'admin@aaradhyadhrma.com' with desired credentials
# Remove or comment out this section after initial setup for security
echo "Checking or updating superuser..."
# Use environment variable for password to avoid hardcoding
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Environment variable DJANGO_SUPERUSER_PASSWORD is set. Proceeding with superuser setup."
    # Create a temporary script to handle non-interactive superuser creation or update
    cat > temp_superuser.py << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'admin'
email = 'admin@aaradhyadhrma.com'
password = '$DJANGO_SUPERUSER_PASSWORD'
try:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"Superuser '{username}' password updated successfully. Staff and superuser status confirmed.")
except User.DoesNotExist:
    user = User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully with staff and superuser status.")
except Exception as e:
    print(f"Error during superuser setup: {str(e)}")
EOF
    python manage.py shell < temp_superuser.py || echo 'Superuser creation or update failed.'
    rm temp_superuser.py
    echo "Superuser creation or update attempted with provided password."
else
    echo "DJANGO_SUPERUSER_PASSWORD environment variable not set. Superuser creation or update will fail without password."
fi
echo "Please ensure DJANGO_SUPERUSER_PASSWORD is set in Render environment variables for secure password setup."

# Start the Gunicorn server
gunicorn aaradhyadhrma.wsgi:application --bind 0.0.0.0:$PORT