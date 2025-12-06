#!/bin/bash
# Quick setup script for AI Terminal Assistant

echo "Setting up AI Terminal Assistant..."
echo ""

# Install dependencies
echo "Installing Python packages..."
pip3 install --user openai python-dotenv

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "Created .env file"
    echo ""
    echo "WARNING: Please edit .env and add your OpenAI API key"
    echo "Get your key from: https://platform.openai.com/api-keys"
else
    echo ".env file already exists"
fi

# Make script executable
echo ""
echo "Making script executable..."
chmod +x ai-terminal.py

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "   1. Edit .env and add your API key"
echo "   2. Run: python3 ai-terminal.py"
echo ""
