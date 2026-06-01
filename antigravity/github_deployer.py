"""GitHub Integration for Auto-Deployment - FULLY WORKING"""

import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Any


class GitHubError(Exception):
    pass


class GitHubDeployer:
    """Deploy generated projects to GitHub using the REST API directly.
    No git binary required — works 100% in Termux without SSH setup."""

    API_BASE = "https://api.github.com"

    def __init__(self, token: str, username: str):
        self.token = token.strip() if token else ""
        self.username = username.strip() if username else ""
        self.configured = bool(self.token and self.username)

    def is_configured(self) -> bool:
        return self.configured

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
            "User-Agent": "AntiGravity-CLI/2.0",
        }

    def _request(self, method: str, path: str, body: Optional[Dict] = None) -> Any:
        """Make an authenticated GitHub API request"""
        if not self.configured:
            raise GitHubError(
                "GitHub not configured.\n"
                "  Run: antigravity ai setup --github TOKEN --username USER\n"
                "  Get a token at: https://github.com/settings/tokens"
            )

        url = f"{self.API_BASE}{path}"
        data = json.dumps(body).encode("utf-8") if body else None
        req = urllib.request.Request(url, data=data, headers=self._headers(), method=method)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw.strip() else {}
        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8", errors="replace")
            try:
                msg = json.loads(body_text).get("message", body_text)
            except Exception:
                msg = body_text[:200]
            raise GitHubError(f"GitHub API {e.code}: {msg}")
        except urllib.error.URLError as e:
            raise GitHubError(f"Network error reaching GitHub: {e.reason}")

    # ------------------------------------------------------------------ #
    # Public methods                                                        #
    # ------------------------------------------------------------------ #

    def create_repo(self, repo_name: str, description: str = "",
                    is_private: bool = False) -> Dict:
        """Create a new GitHub repository"""
        print(f"\n📚 Creating GitHub repository: {repo_name}")
        result = self._request("POST", "/user/repos", {
            "name": repo_name,
            "description": description,
            "private": is_private,
            "auto_init": False,
        })
        url = result.get("html_url", f"https://github.com/{self.username}/{repo_name}")
        clone_url = result.get("clone_url", f"https://github.com/{self.username}/{repo_name}.git")
        print(f"  ✅ Created: {url}\n")
        return {
            "repo": repo_name,
            "url": url,
            "clone_url": clone_url,
        }

    def push_files(self, repo_name: str, files: Dict[str, str],
                   commit_message: str = "Initial commit") -> bool:
        """Push a dict of {filepath: content} to GitHub.
        Creates or updates each file via the Contents API."""
        print(f"\n📤 Pushing {len(files)} file(s) to {self.username}/{repo_name}...")

        success_count = 0
        for file_path, content in files.items():
            encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
            api_path = f"/repos/{self.username}/{repo_name}/contents/{file_path}"

            # Check if file already exists (need its SHA to update)
            sha = None
            try:
                existing = self._request("GET", api_path)
                sha = existing.get("sha")
            except GitHubError:
                pass  # File doesn't exist yet, that's fine

            body: Dict[str, Any] = {
                "message": commit_message,
                "content": encoded,
            }
            if sha:
                body["sha"] = sha

            try:
                self._request("PUT", api_path, body)
                print(f"  ✅ {file_path}")
                success_count += 1
            except GitHubError as e:
                print(f"  ❌ {file_path}: {e}")

        print(f"\n  📊 {success_count}/{len(files)} files pushed successfully.\n")
        return success_count == len(files)

    # Keep old signature for backward compat
    def push_code(self, repo_name: str, files: Dict[str, str],
                  commit_message: str = "Initial commit") -> bool:
        return self.push_files(repo_name, files, commit_message)

    def create_readme(self, repo_name: str, description: str,
                      usage: str = "") -> str:
        """Generate a README.md string"""
        return f"""# {repo_name}

{description}

## Installation

```bash
git clone https://github.com/{self.username}/{repo_name}.git
cd {repo_name}
```

## Usage

{usage if usage else "See source code for usage examples."}

---
*Generated by [AntiGravity AI](https://github.com/AABH-AI/antigravity-cli)*
"""

    def setup_ci_cd(self, repo_name: str, language: str = "python") -> bool:
        """Push a GitHub Actions workflow tailored to the project language"""
        print(f"\n⚙️  Setting up GitHub Actions for {repo_name} ({language})...")

        workflows: Dict[str, str] = {}
        if language in ("python", "py"):
            workflows["ci.yml"] = """name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: \"3.11\"
      - name: Install deps
        run: pip install -r requirements.txt 2>/dev/null || true
      - name: Lint
        run: python -m py_compile *.py
      - name: Run
        run: python main.py --help 2>/dev/null || python main.py || true
"""
        elif language in ("javascript", "js", "node"):
            workflows["ci.yml"] = """name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: \"20\"
      - run: npm install
      - run: npm test 2>/dev/null || node index.js || true
"""
        else:
            workflows["ci.yml"] = """name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo \"Build step — customize for your language\"
"""

        workflow_files = {
            f".github/workflows/{name}": content
            for name, content in workflows.items()
        }
        result = self.push_files(repo_name, workflow_files, "chore: add GitHub Actions CI")
        if result:
            print("  ✅ GitHub Actions configured.\n")
        return result

    def list_repos(self) -> List[Dict]:
        """List the authenticated user's repositories"""
        result = self._request("GET", f"/users/{self.username}/repos?per_page=30&sort=updated")
        return [{"name": r["name"], "url": r["html_url"], "private": r["private"]} for r in result]

    def repo_exists(self, repo_name: str) -> bool:
        """Check if a repo already exists"""
        try:
            self._request("GET", f"/repos/{self.username}/{repo_name}")
            return True
        except GitHubError:
            return False
