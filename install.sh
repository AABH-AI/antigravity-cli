#!/usr/bin/env bash
# AntiGravity AI - Termux Installer
set -e

echo ""
echo "🚀 AntiGravity AI - Termux Installer"
echo "======================================"
echo ""

# ── Dependency checks ──────────────────────────────────────────────────
echo "🔍 Checking dependencies..."

if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "  Installing Python..."
    pkg install python -y
fi

if ! command -v git &>/dev/null; then
    echo "  Installing Git..."
    pkg install git -y
fi

PYTHON=$(command -v python3 || command -v python)
echo "  ✅ Python: $($PYTHON --version)"
echo "  ✅ Git: $(git --version)"
echo ""

# ── Clone ──────────────────────────────────────────────────────────────
INSTALL_DIR="$HOME/antigravity-cli"

if [ -d "$INSTALL_DIR" ]; then
    echo "📥 Updating existing install at $INSTALL_DIR..."
    cd "$INSTALL_DIR"
    git pull --ff-only
else
    echo "📥 Cloning AntiGravity AI..."
    git clone https://github.com/AABH-AI/antigravity-cli.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo ""
echo "📦 Installing AntiGravity CLI..."
$PYTHON -m pip install -e . --quiet

echo ""
echo "✅ Installation complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Quick Start:"
echo ""
echo "  1. Get a FREE Gemini key at https://ai.google.dev"
echo "     Then run:"
echo "     antigravity ai setup --gemini YOUR_GEMINI_KEY"
echo ""
echo "  2. (Optional) Add GitHub for auto-deploy:"
echo "     antigravity ai setup --github YOUR_TOKEN --username YOUR_USERNAME"
echo ""
echo "  3. Check everything works:"
echo "     antigravity ai status"
echo ""
echo "  4. Build your first app:"
echo "     antigravity ai task \"Build a todo app in Python\""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
