# Error Handling Guide

## Philosophy

**Zero Error Tolerance**: Every error is caught, logged, and the user is provided with:
1. Clear explanation of what went wrong
2. Reason why it happened
3. Suggested solution

## Error Types

### Storage Errors

**Message**: "Disk running low (800MB)"

**Causes**:
- Insufficient storage for operation
- Configuration cache full
- Task output logs full

**Solutions**:
```bash
# Check storage
antigravity system storage

# Clear cache
rm -rf ~/.antigravity/cache/*

# View what's taking space
du -sh ~/.antigravity/*
```

### Permission Errors

**Message**: "Permission denied to run this command"

**Causes**:
- Insufficient user permissions
- Task requires root
- Cannot access resource

**Solutions**:
```bash
# Use su (if available)
su -c "antigravity tasks add 'command'"

# Check available permissions
ls -la /path/to/resource

# Request storage permission
termux-setup-storage
```

### Network Errors

**Message**: "No connection detected"

**Causes**:
- Device offline
- Network unavailable
- Remote host unreachable

**Solutions**:
```bash
# Check connection
ping 8.8.8.8

# Use offline mode
antigravity --offline system health

# Try again with retry
antigravity config set max_retries 5
```

### Timeout Errors

**Message**: "Operation took too long (30s)"

**Causes**:
- Slow network
- Heavy system load
- Long-running operation

**Solutions**:
```bash
# Increase timeout
antigravity config set timeout 60

# Run in background
antigravity --verbose tasks add "long-running-command"
```

### Corruption Errors

**Message**: "Cache corrupted, rebuilding..."

**Causes**:
- Unexpected shutdown
- Disk read error
- Corrupted JSON files

**Solutions**:
```bash
# Manual rebuild
rm ~/.antigravity/tasks.json
rm ~/.antigravity/config.json

# Verify installation
pip install --verify antigravity-cli
```

### Dependency Errors

**Message**: "Missing: psutil (required for system info)"

**Causes**:
- Incomplete installation
- Module not installed
- Python version incompatible

**Solutions**:
```bash
# Install missing dependencies
pip install psutil

# Reinstall package
pip install --upgrade -e .

# Check Python version
python --version  # Must be 3.8+
```

### Input Errors

**Message**: "Invalid task ID: task_999"

**Causes**:
- Task doesn't exist
- Wrong syntax
- Typo in command

**Solutions**:
```bash
# List available tasks
antigravity tasks list

# Check command syntax
antigravity tasks --help

# Try again with correct ID
antigravity tasks suspend task_1
```

## Error Logging

All errors are logged in `~/.antigravity/errors.log`

```json
{
  "timestamp": "2026-05-26T16:30:00.123456",
  "context": "Task execution",
  "error_type": "AntiGravityError",
  "message": "Failed to spawn process",
  "traceback": "..."
}
```

## Recovery Strategies

### Automatic Recovery

1. **Network Timeout**: Auto-retry with exponential backoff
2. **Corrupted Cache**: Auto-rebuild from backup
3. **Process Crash**: Auto-restart with preserved state

### Manual Recovery

```bash
# If something goes wrong:

# 1. Check status
antigravity system health

# 2. View logs
cat ~/.antigravity/logs/antigravity-$(date +%Y%m%d).log

# 3. View errors
cat ~/.antigravity/errors.log

# 4. Reset configuration
rm ~/.antigravity/config.json

# 5. Reinstall if necessary
pip install --upgrade --force-reinstall antigravity-cli
```

## Reporting Issues

If you encounter an error:

1. Note the error message
2. Check the error log
3. Try recovery steps above
4. Report issue with:
   - Error message
   - Error log output
   - Steps to reproduce
   - Termux version
   - Android version

Visit: https://github.com/AABH-AI/antigravity-cli/issues
