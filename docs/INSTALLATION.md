# Installation Guide

## Prerequisites

You need:
- Android device
- Termux app (from F-Droid or Google Play)
- Python 3.8+
- Git

## Step-by-Step Installation

### 1. Update Termux

```bash
pkg update
pkg upgrade
```

### 2. Install Dependencies

```bash
pkg install python git
```

### 3. Clone Repository

```bash
git clone https://github.com/AABH-AI/antigravity-cli.git
cd antigravity-cli
```

### 4. Install Package

```bash
pip install -e .
```

### 5. Verify Installation

```bash
antigravity --version
```

## Troubleshooting

### Error: "Command not found: antigravity"

The installation scripts may not have been run. Try:

```bash
python -m antigravity --version
```

Or add to PATH:

```bash
export PATH="$PATH:~/.local/bin"
echo 'export PATH="$PATH:~/.local/bin"' >> ~/.bashrc
```

### Error: "ModuleNotFoundError: psutil"

Reinstall dependencies:

```bash
pip install --upgrade psutil
```

### Permission Denied

Some features require elevated permissions:

```bash
pkg install tsu  # Termux su
su -c "antigravity system battery"
```

## Configuration

Configuration is stored in `~/.antigravity/config.json`

Default values:
```json
{
  "log_level": "INFO",
  "cache_dir": "~/.antigravity/cache",
  "max_retries": 3,
  "timeout": 30,
  "offline_mode": false
}
```

## Updating

```bash
cd antigravity-cli
git pull origin main
pip install --upgrade -e .
```

## Uninstalling

```bash
pip uninstall antigravity-cli
rm -rf ~/.antigravity
rm -rf ~/antigravity-cli
```
