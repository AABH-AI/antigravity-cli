# 🔐 Google Cloud Setup Guide

## Complete Step-by-Step Guide

This guide walks you through setting up Google Cloud integration with AntiGravity CLI.

---

## Part 1: Google Cloud Console

### 1.1 Create Project

**On your desktop/laptop:**

1. Open [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project selector (top of page)
3. Click **NEW PROJECT**
4. Name: `antigravity-cli` (or your choice)
5. Click **CREATE**
6. Wait 1-2 minutes for project creation

### 1.2 Enable Google Drive API

1. Search for "Google Drive API" in the search bar
2. Click **Google Drive API** from results
3. Click **ENABLE**
4. Wait for the API to be enabled

### 1.3 Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials** (left menu)
2. Click **+ CREATE CREDENTIALS**
3. Choose **OAuth 2.0 Client ID**
4. If prompted, click **Configure OAuth Consent Screen**

### 1.4 Configure OAuth Consent Screen

1. Choose **External** user type
2. Click **CREATE**
3. Fill in the form:
   - **App name**: `AntiGravity CLI`
   - **User support email**: Your email
   - **Developer contact**: Your email
4. Click **SAVE AND CONTINUE**
5. Skip scopes, click **SAVE AND CONTINUE**
6. Click **SAVE AND CONTINUE** again
7. Go back to create credentials

### 1.5 Create Desktop Application Credentials

1. Click **+ CREATE CREDENTIALS** again
2. Choose **OAuth 2.0 Client ID**
3. Select **Desktop application**
4. Name: `AntiGravity CLI Termux`
5. Click **CREATE**

### 1.6 Copy Your Credentials

1. A dialog appears with:
   - **Client ID**: Copy this
   - **Client Secret**: Copy this

**Save these values! You'll need them in Termux.**

---

## Part 2: AntiGravity Setup

### 2.1 Configure in Termux

On your Android phone in Termux:

```bash
antigravity google setup \
  --id "YOUR_CLIENT_ID_HERE" \
  --secret "YOUR_CLIENT_SECRET_HERE"
```

**Example:**

```bash
antigravity google setup \
  --id "123456789-abcdefg.apps.googleusercontent.com" \
  --secret "GOCSPX-abcdefghijklmnop"
```

**Output:**
```
✅ Google OAuth2 credentials saved
   📁 ~/.antigravity/google_creds.json

Next: antigravity google auth
```

### 2.2 Authenticate

```bash
antigravity google auth
```

**You'll see:**

```
🔑 Google Authentication

1. Open this URL in your browser:
   https://accounts.google.com/o/oauth2/v2/auth?client_id=...

2. Copy the authorization code
3. Run: antigravity google auth --code YOUR_CODE
```

**Steps:**

1. On your **desktop/laptop**, open the URL in a browser
2. Log in with your Google account
3. Click **Allow** to grant permissions
4. Copy the authorization code
5. In Termux, run:

```bash
antigravity google auth --code "AUTH_CODE_HERE"
```

**Example:**

```bash
antigravity google auth --code "4/0AX4XfWh5..."
```

### 2.3 Verify Authentication

```bash
antigravity google status
```

**Should show:**
```
📊 Authentication Status

Status: authenticated
Message: Authenticated with Google
Obtained: 2026-05-27T15:30:00.123456
```

---

## Part 3: Test & Use

### 3.1 List Google Drive Files

```bash
antigravity google list
```

### 3.2 Check Storage Quota

```bash
antigravity drive quota
```

### 3.3 Upload a File

```bash
antigravity google upload ~/Documents/test.txt
```

### 3.4 Sync Folder

```bash
antigravity drive sync ~/Documents --path "/Backups"
```

---

## Troubleshooting

### Q: "Invalid client"

**A:** Your Client ID or Client Secret is wrong.

- Double-check spelling
- Reconfigure: `antigravity google setup --id ... --secret ...`

### Q: "Authorization code expired"

**A:** Authorization codes expire after 10 minutes.

- Run `antigravity google auth` again
- Complete the flow within 10 minutes

### Q: "Access denied"

**A:** You didn't grant permissions.

- Run `antigravity google auth` again
- Click **Allow** when prompted

### Q: "Rate limit exceeded"

**A:** You're making too many requests.

- Wait a few minutes
- Try again

---

## Security Notes

1. **Never share** your Client ID or Client Secret
2. **Never commit** credentials to git
3. Credentials are stored locally in `~/.antigravity/`
4. You can revoke access in Google Account Settings

---

## Reset/Reconfigure

To start over:

```bash
# Remove credentials
rm ~/.antigravity/google_creds.json
rm ~/.antigravity/google_tokens.json

# Setup again
antigravity google setup --id NEW_ID --secret NEW_SECRET
antigravity google auth
```

---

**You're ready to use Google Drive with AntiGravity!** 🚀
