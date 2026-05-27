# 🜨️ Troubleshooting Guide

## Common Issues & Solutions

---

## Installation Issues

### "Command not found: pip"

**Problem:** pip is not installed

**Solution:**
```bash
pkg install python -y
```

### "Command not found: git"

**Problem:** git is not installed

**Solution:**
```bash
pkg install git -y
```

### "ModuleNotFoundError: No module named 'antigravity'"

**Problem:** AntiGravity is not installed or not in correct directory

**Solution:**
```bash
# Make sure you're in the correct directory
cd antigravity-cli

# Reinstall
pip install -e .

# Verify
antigravity --version
```

### "Permission denied: antigravity"

**Problem:** antigravity script doesn't have execute permission

**Solution:**
```bash
# Use Python module directly
python -m antigravity --version

# Or reinstall
pip install --upgrade -e .
```

---

## Google Authentication Issues

### "Invalid client"

**Problem:** Client ID or Client Secret is incorrect

**Solution:**
1. Double-check your credentials in Google Cloud Console
2. Make sure no extra spaces
3. Reconfigure:
```bash
antigravity google setup --id YOUR_CORRECT_ID --secret YOUR_CORRECT_SECRET
```

### "Authorization code expired"

**Problem:** You took too long (>10 minutes) to get and use the code

**Solution:**
1. Run authentication again:
```bash
antigravity google auth
```
2. Complete the flow within 10 minutes

### "Access denied"

**Problem:** You didn't grant permissions to AntiGravity

**Solution:**
1. Run authentication again:
```bash
antigravity google auth
```
2. When prompted, click **Allow** to grant permissions
3. Continue with the code

### "Credentials not configured"

**Problem:** You skipped the setup step

**Solution:**
```bash
antigravity google setup --id YOUR_ID --secret YOUR_SECRET
antigravity google auth
```

---

## Storage & Permission Issues

### "Permission denied" for storage paths

**Problem:** No access to Android storage

**Solution:**
```bash
# Grant storage permission
termux-setup-storage

# Then check paths
antigravity info storage
```

### "No such file or directory: ~/storage/..."

**Problem:** Storage hasn't been set up

**Solution:**
```bash
# First run
termux-setup-storage

# Verify
ls -la ~/storage

# Should show: downloads, documents, pictures, etc.
```

### "Cannot access Documents"

**Problem:** Documents folder doesn't exist

**Solution:**
```bash
# Create it
mkdir ~/storage/documents

# Verify
antigravity info storage
```

---

## Google Drive Issues

### "Not authenticated with Google"

**Problem:** You're not authenticated

**Solution:**
```bash
antigravity google auth

# Follow the authentication flow
antigravity google auth --code YOUR_CODE

# Verify
antigravity google status
```

### "Rate limit exceeded"

**Problem:** Too many API requests

**Solution:**
- Wait 5-10 minutes
- Try again
- Reduce frequency of operations

### "Drive quota exceeded"

**Problem:** Google Drive storage is full

**Solution:**
```bash
# Check quota
antigravity drive quota

# Delete old files from Google Drive
# Or upgrade your Google account storage
```

### "File upload failed"

**Problem:** Network issue or file too large

**Solution:**
1. Check internet connection
2. Try smaller files first
3. Check file exists:
```bash
ls -la ~/path/to/file
```

---

## Network Issues

### "No internet connection"

**Problem:** WiFi or mobile data is not connected

**Solution:**
1. Check WiFi:
```bash
ping google.com
```
2. Connect to WiFi
3. Try again

### "Connection timeout"

**Problem:** Network is too slow or unstable

**Solution:**
1. Check signal strength
2. Try a different WiFi network
3. Wait and retry
4. Check Google status page

---

## Configuration Issues

### "Cannot find configuration file"

**Problem:** Config files got deleted

**Solution:**
```bash
# Reconfigure from scratch
antigravity google setup --id YOUR_ID --secret YOUR_SECRET
antigravity google auth
```

### "Invalid configuration"

**Problem:** Config file is corrupted

**Solution:**
```bash
# Reset configuration
rm ~/.antigravity/google_creds.json
rm ~/.antigravity/google_tokens.json

# Setup again
antigravity google setup --id YOUR_ID --secret YOUR_SECRET
antigravity google auth
```

---

## Performance Issues

### "Sync is very slow"

**Problem:** Large files or slow connection

**Solution:**
1. Check WiFi speed
2. Sync smaller folders first
3. Try during off-peak hours
4. Check file sizes:
```bash
du -sh ~/Documents
```

### "High CPU usage"

**Problem:** Large sync operation

**Solution:**
1. Wait for sync to complete
2. Don't start new uploads while syncing
3. Restart Termux if needed

---

## Advanced Troubleshooting

### Check Configuration Files

```bash
# List config
ls -la ~/.antigravity/

# View credentials (be careful!)
cat ~/.antigravity/google_creds.json

# Check tokens
cat ~/.antigravity/google_tokens.json
```

### View Logs

```bash
# List available logs
ls -la ~/.antigravity/logs/

# View recent log
cat ~/.antigravity/logs/antigravity.log
```

### Complete Reset

```bash
# Remove all configuration and cache
rm -rf ~/.antigravity/

# Reinstall package
pip uninstall antigravity-cli -y
pip install -e .

# Setup from scratch
antigravity google setup --id YOUR_ID --secret YOUR_SECRET
antigravity google auth
```

---

## Getting Help

If your issue isn't listed:

1. **Check the logs:**
```bash
cat ~/.antigravity/logs/*
```

2. **Run with verbose output:**
```bash
antgravity --help
```

3. **Report an issue:**
   - Go to https://github.com/AABH-AI/antigravity-cli/issues
   - Include error message
   - Include steps to reproduce
   - Include device info:
```bash
antigravity info device
```

---

**Can't find a solution? [Open an issue on GitHub](https://github.com/AABH-AI/antigravity-cli/issues)** 🚀
