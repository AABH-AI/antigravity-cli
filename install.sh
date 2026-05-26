#!/bin/bash

echo "🚀 AntiGravity CLI - Termux Installation Script"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Installing..."
    pkg install python -y
fi

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Installing..."
    pkg install git -y
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Installing..."
    python -m ensurepip
fi

echo "✅ Prerequisites installed"
echo ""

# Clone repository
echo "📥 Cloning repository..."
git clone https://github.com/AABH-AI/antigravity-cli.git
cd antigravity-cli

echo "📦 Installing AntiGravity CLI..."
pip install -e .

echo ""
echo "✅ Installation complete!"
echo ""
echo "Quick start:"
echo "  antigravity --version"
echo "  antigravity --help"
echo "  antigravity tasks --help"
echo "  antigravity clip --help"
echo "  antigravity system --help"
echo ""
echo "More info: https://github.com/AABH-AI/antigravity-cli"
