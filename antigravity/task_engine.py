"""Task Execution Engine"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskEngine:
    """Track and execute AI-generated tasks"""

    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.tasks_file = config_dir / "tasks.json"
        self.tasks: Dict = self._load()

    def _load(self) -> Dict:
        if self.tasks_file.exists():
            try:
                return json.loads(self.tasks_file.read_text())
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save(self) -> None:
        self.tasks_file.parent.mkdir(parents=True, exist_ok=True)
        self.tasks_file.write_text(json.dumps(self.tasks, indent=2, default=str))

    def _next_id(self) -> str:
        n = len(self.tasks) + 1
        return f"task_{n}"

    def create_task(self, description: str, task_type: str = "general") -> str:
        task_id = self._next_id()
        self.tasks[task_id] = {
            "id": task_id,
            "description": description,
            "type": task_type,
            "status": TaskStatus.PENDING.value,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "result": None,
        }
        self._save()
        print(f"\n📋 Task created: {task_id}")
        print(f"   Description: {description}\n")
        return task_id

    def execute_task(self, task_id: str) -> Dict:
        if task_id not in self.tasks:
            return {"error": f"Task '{task_id}' not found. Run: antigravity task list"}

        task = self.tasks[task_id]
        task["status"] = TaskStatus.RUNNING.value
        task["updated_at"] = datetime.now().isoformat()
        self._save()

        print(f"\n▶️  Executing: {task_id}")
        print(f"   {task['description']}\n")

        return {"task_id": task_id, "status": "running"}

    def complete_task(self, task_id: str, result: str = "") -> Dict:
        if task_id not in self.tasks:
            return {"error": f"Task '{task_id}' not found"}

        task = self.tasks[task_id]
        task["status"] = TaskStatus.COMPLETED.value
        task["result"] = result
        task["updated_at"] = datetime.now().isoformat()
        self._save()

        print(f"✅ Task completed: {task_id}\n")
        return task

    def fail_task(self, task_id: str, reason: str = "") -> Dict:
        if task_id not in self.tasks:
            return {"error": f"Task '{task_id}' not found"}

        task = self.tasks[task_id]
        task["status"] = TaskStatus.FAILED.value
        task["result"] = reason
        task["updated_at"] = datetime.now().isoformat()
        self._save()
        return task

    def list_tasks(self, status: Optional[str] = None) -> List[Dict]:
        tasks = list(self.tasks.values())
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        return sorted(tasks, key=lambda t: t.get("created_at", ""))

    def get_task(self, task_id: str) -> Dict:
        return self.tasks.get(task_id, {"error": "Task not found"})
