# 📄 AntiGravity CLI - Usage Guide

## Table of Contents

1. [Basic Commands](#basic-commands)
2. [Google Authentication](#google-authentication)
3. [Google Drive Operations](#google-drive-operations)
4. [Drive Sync](#drive-sync)
5. [System Information](#system-information)
6. [Examples](#examples)

---

## Basic Commands

### Get Help

```bash
# General help
antigravity --help

# Module-specific help
antigravity google --help
antigravity drive --help
antigravity info --help
```

### Check Version

```bash
antigravity --version
# Output: antigravity 1.0.0
```

---

## Google Authentication

### Setup OAuth2

```bash
antigravity google setup --id CLIENT_ID --secret CLIENT_SECRET
```

**Arguments:**
- `--id` (required): Google OAuth2 Client ID
- `--secret` (required): Google OAuth2 Client Secret

**Example:**
```bash
antigravity google setup \
  --id "123456-abc.apps.googleusercontent.com" \
  --secret "GOCSPX-xyz"
```

### Start Authentication

```bash
antigravity google auth
```

**Output:**
```
🔑 Google Authentication

1. Open this URL in your browser:
   https://accounts.google.com/o/oauth2/v2/auth?...

2. Copy the authorization code
3. Run: antigravity google auth --code YOUR_CODE
```

### Complete Authentication with Code

```bash
antigravity google auth --code AUTHORIZATION_CODE
```

**Example:**
```bash
antigravity google auth --code "4/0AX4XfWh5dB..."
```

### Check Authentication Status

```bash
antigravity google status
```

**Output:**
```
📊 Authentication Status

Status: authenticated
Message: Authenticated with Google
Obtained: 2026-05-27T15:30:00.123456
```

---

## Google Drive Operations

### List Files in Google Drive

```bash
antigravity google list
```

**Output:**
```
📄 Google Drive Files

  My Document.docx - 1.2 MB
  Project Folder - Folder
  presentation.pdf - 3.4 MB
```

### Upload File to Google Drive

```bash
antigravity google upload LOCAL_FILE [--path DRIVE_PATH]
```

**Arguments:**
- `LOCAL_FILE` (required): Path to local file
- `--path` (optional): Destination path on Drive (default: "/")

**Examples:**

```bash
# Upload to root
antigravity google upload ~/Documents/report.pdf

# Upload to specific folder
antigravity google upload ~/Documents/report.pdf --path "/Work"

# Upload from downloads
antigravity google upload ~/storage/downloads/photo.jpg --path "/Photos"
```

### Download File from Google Drive

```bash
antigravity google download FILE_ID --output OUTPUT_PATH
```

**Arguments:**
- `FILE_ID` (required): Google Drive file ID
- `--output` (required): Local output path

**Example:**

```bash
antigravity google download "abc123def456" --output ~/Downloads/file.pdf
```

---

## Drive Sync

### Sync Local Folder with Google Drive

```bash
antigravity drive sync LOCAL_FOLDER [--path DRIVE_PATH]
```

**Arguments:**
- `LOCAL_FOLDER` (required): Local folder to sync
- `--path` (optional): Destination on Drive (default: "/")

**Examples:**

```bash
# Sync Documents folder
antigravity drive sync ~/Documents

# Sync to specific Drive folder
antigravity drive sync ~/Documents --path "/Backups"

# Sync Pictures
antigravity drive sync ~/storage/pictures --path "/Photos"
```

### Check Storage Quota

```bash
antigravity drive quota
```

**Output:**
```
📊 Google Drive Quota

  storage_limit: 15 GB
  storage_used: Demo Mode
  message: Actual usage requires authentication
```

### Create Folder on Google Drive

```bash
antigravity drive mkdir NAME [--parent PARENT_ID]
```

**Arguments:**
- `NAME` (required): Folder name
- `--parent` (optional): Parent folder ID (default: "root")

**Examples:**

```bash
# Create root folder
antigravity drive mkdir "My Folder"

# Create nested folder
antigravity drive mkdir "Projects" --parent "parent_folder_id"
```

---

## System Information

### Show Device Information

```bash
antigravity info device
```

**Output:**
```
📱 Device Information

  platform: Termux
  python_version: 3.9.10 (main, ...)
  system: Linux
  machine: aarch64
  running_in_termux: True
```

### Show Available Storage Paths

```bash
antigravity info storage
```

**Output:**
```
📁 Storage Paths

  home: /data/data/com.termux/files/home
  storage: /data/data/com.termux/files/home/storage
  downloads: /data/data/com.termux/files/home/storage/downloads
  documents: /data/data/com.termux/files/home/storage/documents
  pictures: /data/data/com.termux/files/home/storage/pictures
```

---

## Examples

### Example 1: First Time Setup

```bash
# 1. Setup credentials
antigravity google setup \
  --id "YOUR_CLIENT_ID" \
  --secret "YOUR_CLIENT_SECRET"

# 2. Authenticate
antigravity google auth

# Follow the browser-based authentication flow
# 3. Complete with code
antigravity google auth --code "AUTH_CODE"

# 4. Verify
antigravity google status
```

### Example 2: Backup Documents

```bash
# Create backup folder on Drive
antigravity drive mkdir "Phone Backup"

# Sync documents
antigravity drive sync ~/Documents --path "/Phone Backup"

# Check quota
antigravity drive quota
```

### Example 3: Upload Multiple Files

```bash
# Create project folder
antigravity drive mkdir "My Project"

# Upload files
antigravity google upload ~/project/document.pdf --path "/My Project"
antigravity google upload ~/project/images/photo.jpg --path "/My Project"
antigravity google upload ~/project/code.py --path "/My Project"
```

### Example 4: Download and Work with Files

```bash
# List Drive files
antigravity google list

# Download a file
antigravity google download "file_id_123" --output ~/Documents/report.pdf

# Use the file
cat ~/Documents/report.pdf
```

### Example 5: Regular Backups

```bash
# Add to termux startup script
echo 'antigravity drive sync ~/Documents --path "/Daily Backup"' >> ~/.bashrc

# Now every time you open Termux, your documents sync
```

---

## Tips & Tricks

### Quick Alias

```bash
# Add to ~/.bashrc
alias ag='antigravity'
alias ag-sync='antigravity drive sync'
alias ag-up='antigravity google upload'
alias ag-list='antigravity google list'
```

### Batch Upload

```bash
# Upload all files from a directory
for file in ~/Downloads/*; do
  antigravity google upload "$file" --path "/Downloads"
done
```

### Check Before Sync

```bash
# List what's on Drive first
antigravity google list

# Check quota
antigravity drive quota

# Then sync
antigravity drive sync ~/Documents
```

---

**Start using AntiGravity!** 🚀
