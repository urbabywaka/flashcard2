#!/bin/bash

# FlashMaster Setup Script
# This script helps you set up the Django flashcard application

echo "======================================"
echo "  FlashMaster Setup Script"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Install Django
echo "📦 Installing Django..."
pip3 install django --break-system-packages --quiet || pip3 install django --quiet

if [ $? -eq 0 ]; then
    echo "✓ Django installed successfully"
else
    echo "❌ Failed to install Django"
    exit 1
fi

echo ""

# Make migrations
echo "🔨 Creating database migrations..."
python3 manage.py makemigrations accounts
python3 manage.py makemigrations flashcards

echo ""

# Apply migrations
echo "🗄️  Applying migrations to database..."
python3 manage.py migrate

echo ""

# Ask if user wants to create a superuser
echo "👤 Create admin account?"
read -p "Create superuser now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 manage.py createsuperuser
fi

echo ""
echo "======================================"
echo "  ✅ Setup Complete!"
echo "======================================"
echo ""
echo "To start the development server, run:"
echo "  python3 manage.py runserver"
echo ""
echo "Then open your browser to:"
echo "  http://127.0.0.1:8000"
echo ""
echo "Admin panel:"
echo "  http://127.0.0.1:8000/admin"
echo ""
echo "Happy studying! 📚"
