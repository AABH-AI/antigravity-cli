"""Core error handling and utilities"""
import sys
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import traceback

class AntiGravityError(Exception):
    """Base exception for AntiGravity CLI"""
    def __init__(self, message: str, suggestion: str = "", error_code: str = "UNKNOWN"):
        self.message = message
        self.suggestion = suggestion
        self.error_code = error_code
        super().__init__(self.message)

class ErrorHandler:
    """Handles all errors with zero tolerance"""
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.error_log = config_dir / "errors.log"
        self.error_log.parent.mkdir(parents=True, exist_ok=True)
    
    def handle(self, error: Exception, context: str = "") -> int:
        error_data = {"timestamp": datetime.now().isoformat(), "context": context, "error_type": error.__class__.__name__, "message": str(error)}
        with open(self.error_log, "a") as f:
            f.write(json.dumps(error_data) + "\n")
        if isinstance(error, AntiGravityError):
            print(f"❌ {error.message}", file=sys.stderr)
            if error.suggestion:
                print(f"💡 Suggestion: {error.suggestion}", file=sys.stderr)
        else:
            print(f"❌ Unexpected error: {str(error)}", file=sys.stderr)
        return 1

class Config:
    """Configuration management"""
    DEFAULT_CONFIG = {"log_level": "INFO", "cache_dir": "~/.antigravity/cache", "max_retries": 3, "timeout": 30, "offline_mode": False}
    
    def __init__(self):
        self.config_dir = Path.home() / ".antigravity"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.data = self._load()
    
    def _load(self) -> Dict[str, Any]:
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()
    
    def save(self) -> None:
        with open(self.config_file, "w") as f:
            json.dump(self.data, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()

class Logger:
    """Simple logging system"""
    def __init__(self, config_dir: Path):
        self.log_dir = config_dir / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"antigravity-{datetime.now().strftime('%Y%m%d')}.log"
    
    def log(self, message: str, level: str = "INFO") -> None:
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {level}: {message}"
        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")
    
    def info(self, message: str) -> None:
        self.log(message, "INFO")
