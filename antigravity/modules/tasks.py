"""Task/process management module"""
import subprocess
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from ..core import AntiGravityError, Logger

class TaskManager:
    """Manage background tasks with recovery"""
    def __init__(self, config_dir: Path, logger: Logger):
        self.config_dir = config_dir
        self.logger = logger
        self.tasks_file = config_dir / "tasks.json"
        self.tasks_file.parent.mkdir(parents=True, exist_ok=True)
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> Dict:
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_tasks(self) -> None:
        try:
            with open(self.tasks_file, "w") as f:
                json.dump(self.tasks, f, indent=2, default=str)
        except IOError as e:
            raise AntiGravityError(f"Failed to save tasks: {e}", "Check disk space", "STORAGE_ERROR")
    
    def add_task(self, command: str, name: Optional[str] = None) -> str:
        try:
            task_id = f"task_{len(self.tasks) + 1}"
            task_name = name or command[:30]
            try:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                pid = process.pid
                status = "running"
            except PermissionError:
                raise AntiGravityError("Permission denied", "Try: su -c 'antigravity tasks --add \"cmd\"'", "PERMISSION_ERROR")
            self.tasks[task_id] = {"name": task_name, "command": command, "pid": pid, "status": status, "created_at": datetime.now().isoformat()}
            self._save_tasks()
            return task_id
        except Exception as e:
            if isinstance(e, AntiGravityError):
                raise
            raise AntiGravityError(str(e), "", "UNKNOWN")
    
    def list_tasks(self) -> List[Dict]:
        active_tasks = []
        for task_id, task_data in self.tasks.items():
            active_tasks.append({"id": task_id, **task_data})
        return active_tasks
