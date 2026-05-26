# Quick Start Guide

## 30-Second Installation

```bash
pkg install python git
git clone https://github.com/AABH-AI/antigravity-cli.git
cd antigravity-cli
pip install -e .
antigravity --version
```

## 5-Minute Tutorial

### 1. Task Management

```bash
# Start a background task
antigravity tasks add "echo 'Hello' && sleep 1000" --name "Test"

# List tasks
antigravity tasks list
```

### 2. Clipboard

```bash
# Copy text
antigravity clip copy "My important text"

# Get it back
antigravity clip paste

# View history
antigravity clip history
```

### 3. System Health

```bash
# Check everything
antigravity system health
```

## Common Commands

```bash
# Help
antigravity --help
antigravity tasks --help
antigravity clip --help

# Get version
antigravity --version

# Enable verbose output
antigravity --verbose system health
```

## Next Steps

- Read [INSTALLATION.md](docs/INSTALLATION.md) for detailed setup
- Read [USAGE.md](docs/USAGE.md) for all features
- Read [ERRORS.md](docs/ERRORS.md) for error handling

## Get Help

```bash
# Show command help
antigravity <module> --help

# View logs
cat ~/.antigravity/logs/antigravity-*.log

# Check errors
cat ~/.antigravity/errors.log
```

---

**Ready to defy gravity?** 🚀
