#!/bin/bash
set -e

echo "Deployment started ..."

# Pull the latest version of the app
git stash
git pull origin main
echo "New changes copied to server !"

# Activate Virtual Env
source venv/bin/activate
echo "Virtual env 'mb' Activated !"

echo "Installing Dependencies..."
pip3 install -r requirements.txt --no-input

echo "Serving Static Files..."
python3 manage.py collectstatic --noinput

echo "Running Database migration"
python3 manage.py makemigrations
python3 manage.py migrate

# Deactivate Virtual Env
deactivate
echo "Virtual env 'mb' Deactivated !"

# Reloading Application So New Changes could reflect on the website

echo "Deployment Finished!"
