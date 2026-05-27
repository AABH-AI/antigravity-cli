# 🚀 AntiGravity - Complete Setup Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Google Cloud Setup](#google-cloud-setup)
4. [Authentication](#authentication)
5. [Verification](#verification)
6. [Next Steps](#next-steps)

---

## Prerequisites

### Required
- Android device
- [Termux](https://termux.com/) app (from F-Droid or Google Play)
- Internet connection
- Google account

### Recommended
- At least 100MB free storage
- Stable internet connection
- Basic terminal knowledge

---

## Installation

### Step 1: Update Termux

Open Termux and run:

```bash
pkg update && pkg upgrade -y
```

### Step 2: Install Python and Git

```bash
pkg install python git -y
```

Verify installation:

```bash
python --version
git --version
```

### Step 3: Clone Repository

```bash
git clone https://github.com/AABH-AI/antigravity-cli.git
cd antigravity-cli
```

### Step 4: Install AntiGravity

```bash
pip install -e .
```

### Step 5: Verify Installation

```bash
antigravity --version
```

Should output: `antigravity 1.0.0`

---

## Google Cloud Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Create Project**
3. Enter project name (e.g., "AntiGravity CLI")
4. Click **Create**

### Step 2: Enable Google Drive API

1. Search for "Google Drive API"
2. Click **Enable**
3. If prompted, select your project

### Step 3: Create OAuth 2.0 Credentials

1. Go to **Credentials** (left sidebar)
2. Click **Create Credentials** → **OAuth 2.0 Client ID**
3. Choose **Desktop application**
4. Click **Create**
5. You'll see your **Client ID** and **Client Secret**

**⚠️ Important: Keep these private!**

### Step 4: Set Up AntiGravity

In Termux, configure AntiGravity with your credentials:

```bash
antigravity google setup \
  --id "YOUR_CLIENT_ID" \
  --secret "YOUR_CLIENT_SECRET"
```

Replace:
- `YOUR_CLIENT_ID` - Your OAuth2 Client ID
- `YOUR_CLIENT_SECRET` - Your OAuth2 Client Secret

---

## Authentication

### First Time Authentication

1. Run authentication:

```bash
antigravity google auth
```

2. You'll see:

```
🔑 Google Authentication

1. Open this URL in your browser:
   https://accounts.google.com/o/oauth2/v2/auth?...

2. Copy the authorization code
3. Run: antigravity google auth --code YOUR_CODE
```

3. Copy the URL and open in your browser
4. Grant permissions to AntiGravity
5. Copy the authorization code
6. In Termux, complete authentication:

```bash
antigravity google auth --code YOUR_CODE
```

### Subsequent Uses

Once authenticated, your tokens are stored locally. You can use AntiGravity without re-authenticating:

```bash
antigravity google list
antigravity drive quota
```

---

## Verification

### Check Installation

```bash
# Verify CLI works
antigravity --help

# Check Termux integration
antigravity info device

# Check storage access
antigravity info storage
```

### Check Authentication

```bash
# Check auth status
antigravity google status
```

Should show:
```
📊 Authentication Status

Status: authenticated
Message: Authenticated with Google
Obtained: 2026-05-27T...
```

### Test Drive Access

```bash
# List Google Drive files
antigravity google list

# Check storage quota
antigravity drive quota
```

---

## Troubleshooting

### "Command not found: antigravity"

Reinstall the package:

```bash
pip install --upgrade -e .
```

Or use Python module directly:

```bash
python -m antigravity --version
```

### "ModuleNotFoundError: No module named 'antigravity'"

Ensure you're in the correct directory:

```bash
cd antigravity-cli
pip install -e .
```

### "Permission denied" for storage

Grant storage access:

```bash
cd ~/storage
ls -la
```

If nothing appears, run:

```bash
termux-setup-storage
```

### Google authentication fails

Check your credentials:

```bash
cat ~/.antigravity/google_creds.json
```

If missing, reconfigure:

```bash
antigravity google setup --id YOUR_ID --secret YOUR_SECRET
```

---

## Next Steps

1. Read [GOOGLE_SETUP.md](GOOGLE_SETUP.md) for detailed Google Cloud setup
2. Read [USAGE.md](USAGE.md) for command examples
3. Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

---

**You're all set! Start using AntiGravity.** 🚀
