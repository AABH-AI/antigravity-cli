"""Clipboard management module"""
import subprocess
from pathlib import Path
from typing import List
from datetime import datetime
from ..core import AntiGravityError, Logger

class ClipboardManager:
    """Manage clipboard with fallback options"""
    def __init__(self, config_dir: Path, logger: Logger):
        self.config_dir = config_dir
        self.logger = logger
        self.history_file = config_dir / "clipboard_history.txt"
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
    
    def copy(self, text: str) -> None:
        try:
            process = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate(input=text.encode())
            self._add_to_history(text)
            return
        except FileNotFoundError:
            pass
        try:
            temp_clipboard = self.config_dir / ".clipboard"
            with open(temp_clipboard, "w") as f:
                f.write(text)
            self._add_to_history(text)
            return
        except IOError as e:
            raise AntiGravityError(f"Failed to copy: {e}", "Check storage permissions", "CLIPBOARD_ERROR")
    
    def paste(self) -> str:
        try:
            process = subprocess.Popen(["xclip", "-selection", "clipboard", "-o"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()
            return output.decode()
        except FileNotFoundError:
            pass
        try:
            temp_clipboard = self.config_dir / ".clipboard"
            if temp_clipboard.exists():
                with open(temp_clipboard, "r") as f:
                    return f.read()
        except IOError:
            pass
        return ""
    
    def _add_to_history(self, text: str) -> None:
        try:
            timestamp = datetime.now().isoformat()
            with open(self.history_file, "a") as f:
                f.write(f"[{timestamp}] {text[:100]}\n" if len(text) > 100 else f"[{timestamp}] {text}\n")
        except IOError:
            pass
    
    def history(self, limit: int = 10) -> List[str]:
        if not self.history_file.exists():
            return []
        try:
            with open(self.history_file, "r") as f:
                lines = f.readlines()
                return lines[-limit:]
        except IOError:
            return []
