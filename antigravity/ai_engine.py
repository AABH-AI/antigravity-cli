"""Gemini AI Integration for AntiGravity - FULLY WORKING"""

import os
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Dict, Any


class GeminiAIError(Exception):
    """Raised when Gemini API call fails"""
    pass


class GeminiAI:
    """Real Gemini API integration for code generation"""

    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    MODEL = "gemini-1.5-flash"  # Free tier, fast
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds

    def __init__(self, api_key: str):
        self.api_key = api_key.strip() if api_key else ""
        self.configured = bool(self.api_key)

    def is_configured(self) -> bool:
        return self.configured

    def _call_api(self, prompt: str, max_tokens: int = 4096) -> str:
        """Make a real HTTP call to Gemini API with retries"""
        if not self.configured:
            raise GeminiAIError(
                "Gemini API key not set.\n"
                "  Run: antigravity ai setup --gemini YOUR_KEY\n"
                "  Get a free key at: https://ai.google.dev"
            )

        url = self.API_URL.format(model=self.MODEL) + f"?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.2,
            },
        }
        data = json.dumps(payload).encode("utf-8")

        for attempt in range(self.MAX_RETRIES):
            try:
                req = urllib.request.Request(
                    url,
                    data=data,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
                    return result["candidates"][0]["content"]["parts"][0]["text"]

            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", errors="replace")
                if e.code == 429:
                    wait = self.RETRY_DELAY * (attempt + 1)
                    print(f"  ⏳ Rate limited. Waiting {wait}s...")
                    time.sleep(wait)
                    continue
                elif e.code == 403:
                    raise GeminiAIError(
                        f"Invalid or expired API key (HTTP 403).\n"
                        f"  Run: antigravity ai setup --gemini NEW_KEY"
                    )
                else:
                    raise GeminiAIError(f"Gemini API error {e.code}: {body[:200]}")

            except urllib.error.URLError as e:
                if attempt < self.MAX_RETRIES - 1:
                    print(f"  ⚠️  Network error, retrying ({attempt+1}/{self.MAX_RETRIES})...")
                    time.sleep(self.RETRY_DELAY)
                    continue
                raise GeminiAIError(
                    f"Network error: {e.reason}\n"
                    "  Check your internet connection."
                )

            except (KeyError, IndexError, json.JSONDecodeError) as e:
                raise GeminiAIError(f"Unexpected API response format: {e}")

        raise GeminiAIError("Max retries exceeded. Try again later.")

    def generate_code(self, task: str, language: str = "python") -> str:
        """Generate code from natural language description"""
        prompt = f"""You are an expert {language} developer.
Generate complete, runnable {language} code for this task:

Task: {task}

Requirements:
- Write clean, production-ready code
- Include error handling
- Add helpful comments
- Follow {language} best practices
- Include a main() entry point if applicable
- Add a requirements section as a comment if external packages are needed

Respond with ONLY the code. No markdown fences, no explanations."""

        print(f"  🤖 Calling Gemini API...")
        return self._call_api(prompt)

    def build_app(self, app_description: str) -> Dict[str, Any]:
        """Build a complete application - returns dict of filename -> content"""
        prompt = f"""You are a senior full-stack developer.
Design and generate a COMPLETE, working application:

Description: {app_description}

Respond ONLY with a valid JSON object (no markdown, no fences) where:
- Each key is a file path (e.g. "main.py", "utils/helpers.py")
- Each value is the complete file content as a string

Include: main source file(s), requirements.txt or package.json, README.md.
Make it runnable immediately after cloning."""

        print("  🤖 Calling Gemini API to architect app...")
        raw = self._call_api(prompt, max_tokens=8192)

        # Strip markdown fences if model added them anyway
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]

        try:
            files = json.loads(raw)
            if not isinstance(files, dict):
                raise ValueError("Expected a JSON object")
            return {"status": "success", "files": files}
        except (json.JSONDecodeError, ValueError):
            # Fallback: return the raw text as a single file
            return {
                "status": "partial",
                "files": {"generated_app.py": raw},
                "warning": "Could not parse structured output; saved as single file.",
            }

    def fix_code(self, code: str, error: str = "") -> str:
        """Fix buggy code, optionally guided by an error message"""
        error_section = f"\nError message:\n{error}" if error else ""
        prompt = f"""Fix the following code.{error_section}

Code:
{code}

Return ONLY the fixed code with a short comment above each fix explaining what you changed."""

        print("  🤖 Calling Gemini API to fix code...")
        return self._call_api(prompt)

    def review_code(self, code: str) -> str:
        """Review code and return structured suggestions"""
        prompt = f"""Review this code and provide a structured report with these sections:
1. BUGS - actual errors or potential crashes
2. SECURITY - any security issues
3. PERFORMANCE - bottlenecks or inefficiencies
4. STYLE - readability and best practices
5. SUMMARY - overall quality score out of 10 and top 3 recommendations

Code:
{code}"""

        print("  🤖 Calling Gemini API to review code...")
        return self._call_api(prompt)

    def explain_code(self, code: str) -> str:
        """Explain what a piece of code does in plain language"""
        prompt = f"""Explain this code in plain language. Cover:
- What it does overall
- How it works step by step
- Any important patterns or techniques used

Code:
{code}"""
        return self._call_api(prompt)
