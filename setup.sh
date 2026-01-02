#!/bin/bash
# Quick setup script for AI Terminal Assistant
# Optimized for Linux systems

set -e  # Exit on error

echo "=========================================="
echo "  AI Terminal Assistant - Linux Setup"
echo "=========================================="
echo ""

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    echo "Detected Linux distribution: $NAME"
    echo ""
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Install Python 3 using your package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora:        sudo dnf install python3 python3-pip"
    echo "  Arch:          sudo pacman -S python python-pip"
    echo "  OpenSUSE:      sudo zypper install python3 python3-pip"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Using: $PYTHON_VERSION"
echo ""

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    echo ""
    echo "Install pip3 using your package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3-pip"
    echo "  Fedora:        sudo dnf install python3-pip"
    echo "  Arch:          sudo pacman -S python-pip"
    echo ""
    exit 1
fi

# Install dependencies
echo "Installing Python packages..."
if pip3 install --user openai python-dotenv colorama; then
    echo "✓ Packages installed successfully"
else
    echo "ERROR: Failed to install packages"
    echo "Try running manually: pip3 install --user openai python-dotenv colorama"
    exit 1
fi

echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    
    if [ -f env.example ]; then
        cp env.example .env
        echo "✓ Created .env file from env.example"
    elif [ -f .env.example ]; then
        cp .env.example .env
        echo "✓ Created .env file from .env.example"
    else
        # Create default .env file
        cat > .env << 'EOF'
# OpenAI API Key Configuration
OPENAI_API_KEY=your-api-key-here

# Get your API key from:
# https://platform.openai.com/api-keys
EOF
        echo "✓ Created new .env file"
    fi
    
    # Set secure permissions on .env file (Linux best practice)
    chmod 600 .env
    echo "✓ Set secure permissions (600) on .env file"
    echo ""
    echo "⚠ WARNING: Please edit .env and add your OpenAI API key"
    echo "  Get your key from: https://platform.openai.com/api-keys"
    echo "  Edit with: nano .env  (or your preferred editor)"
else
    echo "✓ .env file already exists"
    # Ensure secure permissions
    chmod 600 .env
    echo "✓ Verified secure permissions on .env file"
fi

# Make script executable
echo ""
echo "Making script executable..."
chmod +x ai-terminal.py
echo "✓ ai-terminal.py is now executable"

# Add to PATH suggestion for advanced users
echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your API key:"
echo "     nano .env"
echo ""
echo "  2. Run the assistant:"
echo "     ./ai-terminal.py"
echo "     or"
echo "     python3 ai-terminal.py"
echo ""
echo "Optional - Add alias to your shell (~/.bashrc or ~/.zshrc):"
echo "  alias ai='python3 $(pwd)/ai-terminal.py'"
echo ""
echo "Then reload your shell and use: ai \"your command\""
echo ""
