#!/bin/bash

# First-time setup script for UV-based Python Docker environment
# This script initializes the UV project and creates necessary files

set -e  # Exit on error

echo "=========================================="
echo "UV Python Docker Environment Setup"
echo "=========================================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null
then
    echo "❌ UV is not installed."
    echo ""
    echo "Please install UV using one of the following methods:"
    echo ""
    echo "  Using curl:"
    echo "    curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "  Using pip:"
    echo "    pip install uv"
    echo ""
    exit 1
fi

echo "✅ UV is installed (version: $(uv --version))"
echo ""

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found in the current directory!"
    exit 1
fi

echo "✅ Found requirements.txt"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "🔧 Creating .env file from .env.example..."
        cp .env.example .env
        echo "✅ Created .env file (please review and update values as needed)"
        echo ""
    else
        echo "⚠️  .env.example not found, skipping .env creation"
        echo ""
    fi
else
    echo "✅ .env file already exists"
    echo ""
fi

# Initialize UV project if pyproject.toml doesn't exist
if [ ! -f "pyproject.toml" ]; then
    echo "📦 Initializing UV project..."
    uv init --no-readme
    echo "✅ Created pyproject.toml"
    echo ""
else
    echo "✅ pyproject.toml already exists"
    echo ""
fi

# Add dependencies from requirements.txt
echo "📦 Adding dependencies from requirements.txt..."
uv add --requirements requirements.txt

echo ""
echo "✅ Created/updated uv.lock"
echo ""

echo "=========================================="
echo "Setup complete! 🎉"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Build and start containers: docker-compose up -d"
echo "  2. Or use VS Code Dev Container to open in container"
echo ""
