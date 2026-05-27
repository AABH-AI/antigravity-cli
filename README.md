# 🤖 AntiGravity AI - AI-Powered Development Platform

> **Build Complete Applications with Just Text Descriptions**  
> Transform your ideas into production-ready applications instantly using AI

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Termux Compatible](https://img.shields.io/badge/Termux-Compatible-green)](https://termux.com)
[![Gemini API](https://img.shields.io/badge/Powered%20by-Gemini%20API-orange)](https://ai.google.dev)
[![GitHub Integration](https://img.shields.io/badge/GitHub-Integrated-blue?logo=github)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 What is AntiGravity AI?

**AntiGravity AI** is an AI-powered development platform that runs on your **Android Termux** terminal. It uses **Gemini AI** (or Claude) to:

✨ **Generate code** from natural language descriptions  
🏗️ **Build complete applications** automatically  
📤 **Deploy to GitHub** with one command  
🔄 **Execute tasks** autonomously  
💡 **Review and fix code** intelligently  
📊 **Manage projects** from terminal  

---

## ⚡ Quick Example

Instead of writing code manually:

```bash
antigravity ai task "Build a todo app with Python that saves to JSON"
```

AntiGravity AI will:
1. 🤖 Generate complete Python code
2. 📁 Create project structure
3. 💾 Add dependencies
4. 📤 Deploy to GitHub
5. 🎉 Setup CI/CD

**All in seconds!**

---

## 🎯 Key Features

### 1. 🧠 AI Code Generation
```bash
antigravity code generate "User authentication system"
```
- Generates production-ready code
- Multiple language support
- Best practices included

### 2. 🏗️ App Builder
```bash
antigravity code build "E-commerce website" --name myshop
```
- Complete project structure
- All files generated
- Ready to run

### 3. 📂 Project Management
```bash
antigravity project create myapp python
antigravity project list
antigravity project info myapp
```
- Organize projects
- Track structure
- Manage files

### 4. 🚀 GitHub Deployment
```bash
antigravity deploy repo myapp
antigravity deploy push myapp
antigravity deploy cicd myapp
```
- Auto-create repositories
- Push code automatically
- Setup GitHub Actions

### 5. ✅ Code Review
```bash
antigravity code review mycode.py
antigravity code fix mycode.py --error "TypeError: ..."
```
- Intelligent code review
- Auto-fix errors
- Suggestions

### 6. 📋 Task Management
```bash
antigravity task new "Implement feature X"
antigravity task run task_1
antigravity task list
```
- Track development tasks
- Execute tasks
- Monitor progress

---

## 📥 Installation

### Prerequisites
- Android phone
- Termux app
- Internet connection
- Gemini API key (free)
- GitHub token (optional)

### Step 1: Install

```bash
pkg install python git
git clone https://github.com/AABH-AI/antigravity-cli.git
cd antigravity-cli
pip install -e .
```

### Step 2: Setup AI

```bash
# Get Gemini API key from: https://ai.google.dev
antigravity ai setup --gemini YOUR_GEMINI_KEY

# Optional: Setup GitHub
antigravity ai setup --github YOUR_GITHUB_TOKEN --username YOUR_USERNAME
```

### Step 3: Verify

```bash
antigravity ai status
```

---

## 🎮 Usage Examples

### Example 1: Generate Code

```bash
antigravity code generate "Hello world Flask API" --language python
```

**Output:**
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello, World!'}

if __name__ == '__main__':
    app.run()
```

### Example 2: Build Complete App

```bash
antigravity code build "REST API for managing users" --name userapi
```

**Creates:**
```
userapi/
├── main.py
├── models.py
├── routes.py
├── requirements.txt
└── README.md
```

### Example 3: Deploy to GitHub

```bash
# Create project
antigravity project create myapp python

# Create GitHub repo
antigravity deploy repo myapp --description "My awesome app"

# Push code
antigravity deploy push myapp

# Setup CI/CD
antigravity deploy cicd myapp

# Now it's on GitHub with GitHub Actions!
```

### Example 4: AI Task Execution

```bash
antigravity ai task "Build a weather app that fetches data from OpenWeather API"
```

AI will:
- Generate complete code
- Create project structure
- Add dependencies
- Deploy to GitHub
- Setup CI/CD

---

## 📋 Command Reference

### AI Commands
```bash
antigravity ai setup --gemini KEY --github TOKEN --username USER
antigravity ai status
antigravity ai task "Description"
```

### Code Generation
```bash
antigravity code generate "What to build" [--language LANG] [--output FILE]
antigravity code build "App description" --name APP_NAME
antigravity code fix FILE [--error ERROR_MSG]
antigravity code review FILE
```

### Project Management
```bash
antigravity project create NAME LANGUAGE [--description DESC]
antigravity project list
antigravity project info NAME
```

### Deployment
```bash
antigravity deploy repo NAME [--description DESC] [--private]
antigravity deploy push REPO [--message MSG]
antigravity deploy cicd REPO
```

### Tasks
```bash
antigravity task new "Description" [--type TYPE]
antigravity task list [--status STATUS]
antigravity task run TASK_ID
```

---

## 🔐 Getting API Keys

### Gemini API (Free)
1. Go to [ai.google.dev](https://ai.google.dev)
2. Click "Get API Key"
3. Create new project
4. Generate API key
5. Copy and use:

```bash
antigravity ai setup --gemini YOUR_KEY
```

### GitHub Token
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Create new token
3. Copy and use:

```bash
antigravity ai setup --github YOUR_TOKEN --username YOUR_USERNAME
```

---

## 🎓 Workflow Example

### Day 1: Create Todo App

```bash
# Describe what you want
antigravity ai task "Create a todo app with Python Flask that stores tasks in SQLite"

# AI generates everything automatically
```

### The AI Does:
1. ✅ Generates Flask app code
2. ✅ Creates database models
3. ✅ Adds REST API endpoints
4. ✅ Includes error handling
5. ✅ Creates requirements.txt
6. ✅ Generates README
7. ✅ Creates GitHub repository
8. ✅ Pushes code
9. ✅ Sets up GitHub Actions

### Result:
```
https://github.com/YOUR_USERNAME/todo-app

✅ Complete project on GitHub
✅ Ready to deploy
✅ CI/CD setup
✅ Fully documented
```

---

## 💡 Advanced Features

### Batch Tasks
```bash
antigravity task new "Feature 1"
antigravity task new "Feature 2"
antigravity task new "Feature 3"
antigravity task list
```

### Code Review Workflow
```bash
antigravity code review mycode.py
# Get suggestions from AI
antigravity code fix mycode.py
# Auto-fix issues
antigravity code review mycode.py
# Verify improvements
```

### Multi-Language Projects
```bash
antigravity project create backend python
antigravity project create frontend javascript
antigravity code generate "API endpoint" --language python
antigravity code generate "React component" --language javascript
```

---

## 🧪 Testing

GitHub Actions automatically tests all generated code.

---

## 📚 Documentation

- **[HOW_TO_RUN.md](HOW_TO_RUN.md)** - Setup and installation
- **[USAGE.md](USAGE.md)** - Complete command reference
- **[EXAMPLES.md](EXAMPLES.md)** - Detailed examples

---

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

- Powered by **Google Gemini API**
- Built for **Termux**
- Integrates with **GitHub**
- Made for developers

---

## 🚀 Ready to Build?

```bash
antigravity ai status
antigravity ai task "Your awesome idea here"
```

**Your idea → AI code → GitHub repository → Done! 🎉**

---

**Build smarter, not harder. AntiGravity AI.** 🤖
