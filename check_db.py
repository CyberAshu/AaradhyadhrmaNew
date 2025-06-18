import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_root = str(Path(__file__).resolve().parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aaradhyadhrma.settings')
django.setup()

# Now we can import settings after Django setup
from django.conf import settings

print("Current database configuration:")
print(f"DB_ENGINE: {settings.DATABASES['default']['ENGINE']}")
print(f"DB_NAME: {settings.DATABASES['default']['NAME']}")
print(f"DB_USER: {settings.DATABASES['default']['USER']}")
print(f"DB_HOST: {settings.DATABASES['default']['HOST']}")
print(f"DB_PORT: {settings.DATABASES['default']['PORT']}")

# Also print environment variables to verify
try:
    print("\nEnvironment variables:")
    for key in ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']:
        print(f"{key}: {os.environ.get(key, 'Not set')}")
except Exception as e:
    print(f"Error reading environment variables: {e}")
