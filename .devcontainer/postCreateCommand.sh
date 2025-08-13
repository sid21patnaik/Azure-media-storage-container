#!/bin/bash
echo "🚀 Setting up Python virtual environment..."

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Virtual environment created."
else
    echo "ℹ️ Virtual environment already exists."
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed from requirements.txt"
else
    echo "⚠️ No requirements.txt found — skipping dependency installation."
fi

# Add venv auto-activation to .bashrc
if ! grep -q "source .venv/bin/activate" ~/.bashrc; then
    echo "source .venv/bin/activate" >> ~/.bashrc
    echo "✅ Added auto venv activation to .bashrc"
fi

echo "🎯 Environment setup complete."
