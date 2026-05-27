"""Task Execution Engine"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskEngine:
    """Execute AI-generated tasks"""
    
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.tasks_file = config_dir / "tasks.json"
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> Dict:
        """Load task history"""
        if self.tasks_file.exists():
            with open(self.tasks_file) as f:
                return json.load(f)
        return {}
    
    def _save_tasks(self) -> None:
        """Save task history"""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2, default=str)
    
    def create_task(self, description: str, task_type: str) -> str:
        """Create new task"""
        task_id = f"task_{len(self.tasks) + 1}"
        
        self.tasks[task_id] = {
            'description': description,
            'type': task_type,
            'status': TaskStatus.PENDING.value,
            'created_at': str(__import__('datetime').datetime.now())
        }
        self._save_tasks()
        
        print(f"\n📋 Task created: {task_id}")
        print(f"   Description: {description}")
        print(f"   Type: {task_type}\n")
        
        return task_id
    
    def execute_task(self, task_id: str) -> Dict:
        """Execute a task"""
        if task_id not in self.tasks:
            return {'error': f'Task {task_id} not found'}
        
        task = self.tasks[task_id]
        task['status'] = TaskStatus.RUNNING.value
        self._save_tasks()
        
        print(f"\n▶️  Executing task: {task_id}")
        print(f"   Description: {task['description']}")
        print(f"   Type: {task['type']}")
        print(f"   ✅ Task execution started\n")
        
        return {
            'task_id': task_id,
            'status': 'running',
            'message': 'Task is executing...'
        }
    
    def complete_task(self, task_id: str, result: str = "") -> Dict:
        """Mark task as completed"""
        if task_id not in self.tasks:
            return {'error': f'Task {task_id} not found'}
        
        task = self.tasks[task_id]
        task['status'] = TaskStatus.COMPLETED.value
        task['result'] = result
        self._save_tasks()
        
        print(f"\n✅ Task completed: {task_id}\n")
        
        return task
    
    def list_tasks(self, status: Optional[str] = None) -> List[Dict]:
        """List tasks"""
        tasks = list(self.tasks.values())
        
        if status:
            tasks = [t for t in tasks if t['status'] == status]
        
        return tasks
    
    def get_task(self, task_id: str) -> Dict:
        """Get task details"""
        return self.tasks.get(task_id, {'error': 'Task not found'})
