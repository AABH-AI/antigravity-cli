# Usage Guide

## Command Structure

```
antigravity <module> <action> [options]
```

## Available Modules

### 1. Tasks Module

Manage background processes and tasks.

```bash
# Add a new task
antigravity tasks add "npm start" --name "Development Server"

# List all tasks
antigravity tasks list

# Suspend a task
antigravity tasks suspend task_1

# Resume a task
antigravity tasks resume task_1
```

**Use Cases:**
- Run long-running processes in background
- Monitor multiple tasks
- Pause/resume tasks without killing them

### 2. Clipboard Module

Manage clipboard content with history and search.

```bash
# Copy to clipboard
antigravity clip copy "Hello, World!"

# Paste from clipboard
antigravity clip paste

# View clipboard history (last 10 items)
antigravity clip history

# View last 20 items
antigravity clip history --limit 20

# Search clipboard history
antigravity clip search "important"
```

**Use Cases:**
- Quick access to frequently copied text
- Search through clipboard history
- Share clipboard content

### 3. System Module

Monitor system resources and health.

```bash
# System health check
antigravity system health

# Storage information
antigravity system storage

# Memory information
antigravity system memory

# Battery status
antigravity system battery
```

**Output Example:**
```
📊 System Health Report

Storage: 5.2GB / 50GB (10.4%)
Memory: 2048MB / 4096MB (50%)
Battery: 85%

✅ All systems normal
```

### 4. Config Module

Manage application configuration.

```bash
# Show all configuration
antigravity config show

# Set a configuration value
antigravity config set log_level DEBUG

# Set offline mode
antigravity config set offline_mode true
```

## Global Options

```bash
# Show version
antigravity --version

# Enable verbose output
antigravity --verbose tasks list

# Run in offline mode
antigravity --offline tasks add "command"
```

## Examples

### Example 1: Development Workflow

```bash
# Start development server in background
antigravity tasks add "npm start" --name "Dev Server"

# Start test watcher
antigravity tasks add "npm test -- --watch" --name "Tests"

# Check status
antigravity tasks list

# Pause tests while working
antigravity tasks suspend task_2

# Resume tests
antigravity tasks resume task_2
```

### Example 2: System Monitoring

```bash
# Check overall health
antigravity system health

# If storage is low, check what's using space
antigravity system storage

# Monitor battery
antigravity system battery
```

### Example 3: Clipboard Management

```bash
# Save API key (temporarily)
antigravity clip copy "sk_live_1234567890"

# View history
antigravity clip history

# Paste when needed
antigravity clip paste

# Clear after use (optional)
echo "" | antigravity clip copy
```

## Error Handling

AntiGravity CLI handles errors gracefully:

```bash
# If task already exists
$ antigravity tasks add "npm start"
❌ Task already running (PID: 1234)
💡 Suggestion: Use 'antigravity tasks suspend task_1' to pause it

# If storage is low
$ antigravity system storage
⚠️  Storage running low (800MB free)
💡 Suggestion: Check /sdcard for large files

# Invalid command
$ antigravity invalid command
❌ Unknown module: invalid
💡 Suggestion: Try 'antigravity --help'
```

## Logs and Debugging

```bash
# View logs
cat ~/.antigravity/logs/antigravity-$(date +%Y%m%d).log

# View errors
cat ~/.antigravity/errors.log

# Enable verbose output for debugging
antigravity --verbose system health
```
