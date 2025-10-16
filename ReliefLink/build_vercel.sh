#!/bin/bash
# Build script for Vercel deployment

echo "====== Starting Vercel Build ======"
echo "Python version:"
python --version

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear --verbosity=2

echo ""
echo "Listing staticfiles directory:"
ls -la staticfiles/ || echo "staticfiles directory not found!"

echo ""
echo "Listing staticfiles/home:"
ls -la staticfiles/home/ || echo "staticfiles/home not found!"

echo ""
echo "====== Build Complete ======"
