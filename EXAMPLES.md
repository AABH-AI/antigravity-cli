# 📖 AntiGravity AI - Examples

## Example 1: Simple Web Server

```bash
antigravity code generate "Python Flask web server with index page"
```

## Example 2: Complete Todo App

```bash
antigravity code build "Todo application with add, delete, mark complete features. Store in SQLite." --name todoapp

antigravity deploy repo todoapp --description "A simple todo application"
antigravity deploy push todoapp
antigravity deploy cicd todoapp

# Now your app is on GitHub!
```

## Example 3: REST API

```bash
antigravity ai task "Build a REST API using FastAPI that manages users. Include endpoints for create, read, update, delete. Store in PostgreSQL."
```

## Example 4: Code Review Workflow

```bash
# Review your code
antigravity code review mycode.py

# AI suggests improvements, then fix it
antigravity code fix mycode.py --error "Function too long"

# Review again
antigravity code review mycode.py
```

## Example 5: Multi-File Project

```bash
# Create project
antigravity project create ecommerce python

# Generate different modules
antigravity code generate "User authentication module" --output ecommerce/auth.py
antigravity code generate "Product catalog module" --output ecommerce/products.py
antigravity code generate "Shopping cart module" --output ecommerce/cart.py

# Deploy
antigravity deploy repo ecommerce
antigravity deploy push ecommerce
```

---

See [HOW_TO_RUN.md](HOW_TO_RUN.md) for more details.
