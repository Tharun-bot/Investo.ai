#!/bin/bash

echo "Setting up Investo.ai Django Project..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

# Collect static files
python manage.py collectstatic --noinput

echo "Setup complete! Run 'python manage.py runserver' to start the development server."
