#!/usr/bin/env bash
# Quick start script for Aaradhyadhrma website
# Created by Cascade

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Aaradhyadhrma Website - Quick Start${NC}"
echo -e "${BLUE}========================================${NC}"

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
. venv/bin/activate || source venv/bin/activate

# Check for migrations
echo -e "${YELLOW}Checking for database migrations...${NC}"
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput

# Start development server
echo -e "${YELLOW}Starting development server...${NC}"
echo -e "${GREEN}Access the website at: http://127.0.0.1:8000/${NC}"
echo -e "${GREEN}Access the admin panel at: http://127.0.0.1:8000/admin/${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo -e "${BLUE}========================================${NC}"

python manage.py runserver
