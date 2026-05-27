# 🚀 How to Use AntiGravity AI

> Complete guide to building apps with AI

---

## Installation (5 Minutes)

```bash
# 1. Install
pkg install python git

# 2. Clone
git clone https://github.com/AABH-AI/antigravity-cli.git
cd antigravity-cli

# 3. Install package
pip install -e .

# 4. Verify
antigravity ai status
```

---

## Get API Keys

### Gemini API (Required)
1. Go to [ai.google.dev](https://ai.google.dev)
2. Click "Get API Key"
3. Create project
4. Copy key

### GitHub (Optional)
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Create token
3. Copy token and username

---

## Setup

```bash
antigravity ai setup --gemini YOUR_GEMINI_KEY

# Optional:
antigravity ai setup --github YOUR_GITHUB_TOKEN --username YOUR_USERNAME
```

---

## Basic Usage

### Generate Code
```bash
antigravity code generate "Hello world app"
```

### Build Application
```bash
antigravity code build "Todo app" --name mytodo
```

### Create Project
```bash
antigravity project create myapp python
```

### Deploy to GitHub
```bash
antigravity deploy repo myapp
antigravity deploy push myapp
```

### Manage Tasks
```bash
antigravity task new "Build feature"
antigravity task list
antigravity task run task_1
```

---

## Complete Workflow

```bash
# 1. Describe what you want
antigravity ai task "Build a REST API for managing books"

# AI automatically:
# - Generates code
# - Creates project structure
# - Adds dependencies
# - Creates GitHub repo
# - Pushes code
# - Sets up CI/CD

# 2. Check status
antigravity ai status

# 3. View projects
antigravity project list

# 4. View tasks
antigravity task list
```

---

## Examples

See [EXAMPLES.md](EXAMPLES.md) for detailed examples.

---

**Start building with AI!** 🤖
