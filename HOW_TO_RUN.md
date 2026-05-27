# 🚀 HOW TO RUN ANTIGRAVITY CLI

> **Complete guide to installing and using AntiGravity CLI on your Android Termux phone**

---

## 📋 Quick Overview

**What is AntiGravity CLI?**
- A terminal utility for Termux (Android)
- Integrates with Google Drive and Google Cloud
- Manage files, upload, download, sync
- All from your Android terminal

**Requirements:**
- Android phone
- Termux app (free)
- Internet connection
- Google account

---

## ⚡ Installation (5 Minutes)

### Step 1: Open Termux

Open the Termux app on your Android phone.

### Step 2: Update Termux

Run this command:

```bash
pkg update && pkg upgrade -y
```

This downloads the latest packages. It may take 1-2 minutes.

### Step 3: Install Python and Git

Run this command:

```bash
pkg install python git -y
```

Answer `y` when prompted.

### Step 4: Clone AntiGravity

Run this command:

```bash
git clone https://github.com/AABH-AI/antigravity-cli.git
cd antigravity-cli
```

This downloads AntiGravity to your phone.

### Step 5: Install AntiGravity

Run this command:

```bash
pip install -e .
```

### Step 6: Verify Installation

Run this command:

```bash
antigravity --version
```

You should see: `antigravity 1.0.0`

**✅ Installation complete!**

---

## 🔐 Google Cloud Setup (10 Minutes)

### Step 1: Get Google Credentials (On Desktop/Laptop)

1. Open your browser
2. Go to [Google Cloud Console](https://console.cloud.google.com/)
3. Click **Create Project**
4. Name it: `antigravity-cli`
5. Click **Create**
6. Wait 1-2 minutes

### Step 2: Enable Google Drive API

1. Search for "Google Drive API"
2. Click **Enable**

### Step 3: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **OAuth 2.0 Client ID**
3. If prompted, click **Configure OAuth Consent Screen**
   - Choose **External**
   - Fill in app name: `AntiGravity CLI`
   - Enter your email
   - Click **Save and Continue** (skip other screens)
4. Create credentials:
   - Application type: **Desktop application**
   - Name: `AntiGravity CLI`
   - Click **Create**

### Step 4: Copy Credentials

You'll see:
- **Client ID** (looks like: `123456789-abc.apps.googleusercontent.com`)
- **Client Secret** (looks like: `GOCSPX-xyz...`)

**Copy both and save them!**

### Step 5: Configure in Termux

In Termux on your phone, run:

```bash
antigravity google setup \
  --id "YOUR_CLIENT_ID" \
  --secret "YOUR_CLIENT_SECRET"
```

Replace with your actual credentials.

**Example:**
```bash
antigravity google setup \
  --id "123456789-abc.apps.googleusercontent.com" \
  --secret "GOCSPX-abcdefg123"
```

### Step 6: Authenticate

In Termux, run:

```bash
antigravity google auth
```

You'll see a URL. Copy it and open in your browser.

1. Click **Allow** to grant permissions
2. Copy the authorization code
3. In Termux, run:

```bash
antigravity google auth --code "YOUR_CODE"
```

### Step 7: Verify

In Termux, run:

```bash
antigravity google status
```

You should see: `Status: authenticated`

**✅ Google setup complete!**

---

## 🎮 Using AntiGravity

### List Google Drive Files

```bash
antigravity google list
```

### Upload File

```bash
antigravity google upload ~/Documents/myfile.txt
```

### Download File

```bash
antigravity google download FILE_ID --output ~/Documents/myfile.txt
```

### Sync Folder

```bash
antigravity drive sync ~/Documents
```

### Check Storage

```bash
antigravity drive quota
```

### View Storage Paths

```bash
antigravity info storage
```

### Get Help

```bash
antigravity --help
antigravity google --help
antigravity drive --help
```

---

## 📚 Common Workflows

### Workflow 1: Backup Documents

```bash
# Sync your documents to Google Drive
antigravity drive sync ~/Documents --path "/Phone Backup"
```

### Workflow 2: Upload Screenshots

```bash
# Upload all screenshots
for file in ~/storage/pictures/*.png; do
  antigravity google upload "$file" --path "/Screenshots"
done
```

### Workflow 3: Download Project Files

```bash
# Check what's on Drive
antigravity google list

# Download a file
antigravity google download "file_id" --output ~/Documents/file.zip
```

---

## ⚠️ Troubleshooting

### "Command not found: antigravity"

**Solution:**
```bash
# Reinstall
pip install -e .

# Or use:
python -m antigravity --version
```

### "Permission denied" for storage

**Solution:**
```bash
# Grant storage access
termux-setup-storage

# Then check:
ls -la ~/storage
```

### "Invalid client" error

**Solution:**
- Double-check Client ID and Secret
- No extra spaces
- Reconfigure:
```bash
antigravity google setup --id YOUR_ID --secret YOUR_SECRET
```

### "Not authenticated"

**Solution:**
```bash
antigravity google auth
# Follow the browser authentication flow
antigravity google auth --code YOUR_CODE
```

---

## 📖 Full Documentation

- **[README.md](README.md)** - Project overview
- **[SETUP.md](SETUP.md)** - Installation guide
- **[GOOGLE_SETUP.md](GOOGLE_SETUP.md)** - Google Cloud setup
- **[USAGE.md](USAGE.md)** - Complete command reference
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Problem solving

---

## 🎯 What You Can Do Now

✅ Access Google Drive from Termux  
✅ Upload files from your phone  
✅ Download files to your phone  
✅ Sync folders automatically  
✅ Check storage quota  
✅ Manage files via command line  

---

## 🔒 Security Tips

1. **Never share** Client ID or Secret
2. **Credentials stored** in `~/.antigravity/` (local only)
3. **Can revoke access** anytime in Google Account
4. **Don't commit** credentials to git

---

## 💡 Next Steps

1. Set up Google credentials (if not done)
2. Try uploading a file
3. Set up automatic syncing
4. Read full documentation

---

## ❓ Questions?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Open issue on [GitHub](https://github.com/AABH-AI/antigravity-cli/issues)
- Read [USAGE.md](USAGE.md) for examples

---

## 🎉 You're Ready!

Your Termux phone now has a powerful cloud-integrated CLI tool.

**Start by uploading a file:**

```bash
antigravity google upload ~/Documents/test.txt
```

**Made for Termux. By developers, for developers.** 🚀
