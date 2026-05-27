# 🚀 AntiGravity CLI

> **Termux + Google Cloud Integration** - Powerful terminal utilities for your Android phone

[![Tests](https://github.com/AABH-AI/antigravity-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/AABH-AI/antigravity-cli/actions)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Termux Compatible](https://img.shields.io/badge/Termux-Compatible-green)](https://termux.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-AABH--AI-blue?logo=github)](https://github.com/AABH-AI/antigravity-cli)

---

## 🌟 Overview

**AntiGravity CLI** is a powerful command-line tool designed for **Termux on Android** that seamlessly integrates with **Google Cloud services** (Google Drive, Cloud Storage, etc.). Access your files, manage projects, and leverage cloud services directly from your Android terminal.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔐 **Google OAuth2** | Secure authentication with Google Cloud |
| 📄 **Google Drive** | Upload, download, sync files and folders |
| 📋 **File Management** | Manage files across Termux and cloud |
| 📱 **Android Native** | Full Termux integration with storage access |
| 🔧 **CLI Tools** | Powerful command-line interface |
| ✅ **Production Ready** | Tested and optimized for Android |

---

## 🚀 Quick Start

### Installation (3 Commands)

```bash
# 1. Install Python and Git
pkg install python git

# 2. Clone and install
git clone https://github.com/AABH-AI/antigravity-cli.git
cd antigravity-cli
pip install -e .

# 3. Verify installation
antigravity --version
# Output: antigravity 1.0.0
```

### First Steps

```bash
# Check Termux integration
antigravity info device

# View available storage paths
antigravity info storage

# Get help
antigravity --help
```

---

## 🔐 Google Cloud Setup

### Step 1: Get Google Cloud Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Drive API
4. Create OAuth 2.0 credentials (Desktop Application)
5. Copy your **Client ID** and **Client Secret**

### Step 2: Configure AntiGravity

```bash
# Setup with your credentials
antigravity google setup --id "YOUR_CLIENT_ID" --secret "YOUR_CLIENT_SECRET"

# Output:
# ✅ Google OAuth2 credentials saved
#    📁 ~/.antigravity/google_creds.json
```

### Step 3: Authenticate

```bash
# Start authentication
antigravity google auth

# Follow the prompts:
# 1. Open the URL in your browser
# 2. Grant permissions
# 3. Copy the authorization code
# 4. Run: antigravity google auth --code YOUR_CODE
```

### Step 4: Verify

```bash
# Check authentication status
antigravity google status

# Output:
# 📊 Authentication Status
# Status: authenticated
# Message: Authenticated with Google
```

---

## 📄 Google Drive Operations

### List Files

```bash
antigravity google list
```

### Upload Files

```bash
# Upload single file
antigravity google upload ~/Downloads/document.pdf

# Upload to specific folder
antigravity google upload ~/Downloads/document.pdf --path "/My Folder"
```

### Download Files

```bash
antigravity google download FILE_ID --output ~/Downloads/file.pdf
```

### Sync Folders

```bash
# Sync local folder with Google Drive
antigravity drive sync ~/Documents --path "/Backups"
```

### Check Storage Quota

```bash
antigravity drive quota
```

---

## 📱 Termux Integration

### Storage Access

```bash
# Grant storage permissions (run once)
antgravity info storage

# This will show accessible paths:
# home: /data/data/com.termux/files/home
# storage: /data/data/com.termux/files/home/storage
# downloads: /data/data/com.termux/files/home/storage/downloads
# documents: /data/data/com.termux/files/home/storage/documents
```

### Device Information

```bash
# Get device and Termux info
antigravity info device
```

### Storage Paths

```bash
# View all available storage paths
antigravity info storage
```

---

## 📚 Complete Command Reference

### Google Authentication

```bash
# Setup OAuth2 credentials
antigravity google setup --id CLIENT_ID --secret CLIENT_SECRET

# Start authentication flow
antigravity google auth

# Complete authentication with code
antigravity google auth --code AUTHORIZATION_CODE

# Check authentication status
antigravity google status
```

### Google Drive

```bash
# List files in Drive
antigravity google list

# Upload file
antigravity google upload LOCAL_FILE [--path DRIVE_PATH]

# Download file
antigravity google download FILE_ID --output OUTPUT_PATH
```

### Drive Operations

```bash
# Sync folder with Drive
antigravity drive sync LOCAL_FOLDER [--path DRIVE_PATH]

# Check storage quota
antigravity drive quota

# Create folder on Drive
antigravity drive mkdir "Folder Name" [--parent PARENT_ID]
```

### System Information

```bash
# Show device information
antigravity info device

# Show available storage paths
antigravity info storage
```

---

## 💾 Configuration

Configuration is stored in `~/.antigravity/`:

```
~/.antigravity/
├── google_creds.json      # OAuth2 credentials
├── google_tokens.json     # Auth tokens
├── drive_cache/           # Cached Drive files
├── logs/                  # Application logs
└── config.json            # Main configuration
```

---

## 📚 Documentation

| Document | Purpose |
|----------|----------|
| [SETUP.md](SETUP.md) | Detailed setup and installation |
| [GOOGLE_SETUP.md](GOOGLE_SETUP.md) | Step-by-step Google Cloud configuration |
| [USAGE.md](USAGE.md) | Complete usage guide with examples |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and solutions |

---

## 🔣 Examples

### Example 1: Backup Documents to Google Drive

```bash
# Sync your Documents folder to Google Drive
antigravity drive sync ~/Documents --path "/Mobile Backups"
```

### Example 2: Download Project Files

```bash
# List files in Drive
antigravity google list

# Download a specific file
antigravity google download "file_id_here" --output ~/Documents/project.zip
```

### Example 3: Upload Screenshots

```bash
# Upload screenshots to Drive
antigravity google upload ~/storage/pictures/screenshot.png --path "/Screenshots"
```

---

## 🜨️ Troubleshooting

### Storage Access Issues

```bash
# If you get "Permission Denied"
cd ~/storage

# Or setup storage access:
ls -la ~/storage
```

### Google Authentication Issues

```bash
# Check credentials file
cat ~/.antigravity/google_creds.json

# Check if authenticated
antigravity google status

# Re-authenticate if needed
antigravity google setup --id NEW_ID --secret NEW_SECRET
antigravity google auth
```

### Sync Issues

```bash
# Clear cache and retry
rm -rf ~/.antigravity/drive_cache/*
antigravity drive sync ~/Documents
```

---

## 📦 Project Structure

```
antigravity/
├── __init__.py              # Package init
├── __main__.py              # Entry point
├── cli.py                   # Main CLI interface
├── google_auth.py          # Google OAuth2
├── google_drive.py         # Google Drive operations
└── termux_utils.py         # Termux utilities

.
├── setup.py                # Installation config
├── requirements.txt        # Dependencies
├── README.md               # This file
├── SETUP.md                # Setup guide
├── GOOGLE_SETUP.md         # Google setup
├── USAGE.md                # Usage guide
├── TROUBLESHOOTING.md      # Troubleshooting
└── .github/
    └── workflows/
        └── tests.yml       # GitHub Actions tests
```

---

## 👩‍💻 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📁 License

MIT License - See [LICENSE](LICENSE) for details

---

## 📄 Support

- **Issues**: [GitHub Issues](https://github.com/AABH-AI/antigravity-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AABH-AI/antigravity-cli/discussions)
- **Wiki**: [GitHub Wiki](https://github.com/AABH-AI/antigravity-cli/wiki)

---

## 🚀 Roadmap

- [x] Google OAuth2 authentication
- [x] Google Drive file operations
- [x] Termux integration
- [ ] Google Cloud Storage support
- [ ] Google Sheets integration
- [ ] Google Photos backup
- [ ] Cloud SQL support
- [ ] Advanced sync options
- [ ] Web dashboard
- [ ] Mobile app companion

---

## 🐟 Acknowledgments

Built for the Termux community with ❤️

---

## 🚀 Ready to Defy Gravity?

```bash
git clone https://github.com/AABH-AI/antigravity-cli.git
cd antigravity-cli
pip install -e .
antigravity --version
```

**Start uploading from your phone today!** 📁⬆️

---

**Made for Termux. By developers, for developers.** 🚀
