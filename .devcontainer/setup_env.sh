#!/bin/bash
echo "🔄 Pulling latest changes..."
git pull origin $(git rev-parse --abbrev-ref HEAD)

echo "🔧 Running Codespace environment setup..."
bash .devcontainer/postCreateCommand.sh

source ~/.bashrc

echo "✅ Environment is now up to date."
