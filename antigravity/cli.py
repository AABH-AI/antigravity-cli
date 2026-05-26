"""Command-line interface"""
import sys
import argparse
from pathlib import Path
from typing import Optional
from .core import Config, Logger, ErrorHandler, AntiGravityError
from .modules.tasks import TaskManager
from .modules.clipboard import ClipboardManager
from .modules.system_info import SystemInfo

class AntiGravityCLI:
    """Main CLI application"""
    def __init__(self):
        self.config_dir = Path.home() / ".antigravity"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config = Config()
        self.logger = Logger(self.config_dir)
        self.error_handler = ErrorHandler(self.config_dir)
        self.task_manager = TaskManager(self.config_dir, self.logger)
        self.clipboard_manager = ClipboardManager(self.config_dir, self.logger)
        self.system_info = SystemInfo(self.logger)
    
    def run(self, args: Optional[list] = None) -> int:
        try:
            parser = self._create_parser()
            parsed_args = parser.parse_args(args)
            if hasattr(parsed_args, 'func'):
                return parsed_args.func(parsed_args) or 0
            else:
                parser.print_help()
                return 0
        except AntiGravityError as e:
            return self.error_handler.handle(e, "CLI execution")
        except KeyboardInterrupt:
            print("\n⚠️  Operation cancelled", file=sys.stderr)
            return 130
        except Exception as e:
            return self.error_handler.handle(e, "Unexpected error")
    
    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog="antigravity", description="🚀 AntiGravity CLI - Defying gravity on Termux")
        parser.add_argument("--version", "-v", action="version", version="%(prog)s 0.1.0")
        subparsers = parser.add_subparsers(title="modules", dest="module")
        self._add_tasks_commands(subparsers)
        self._add_clipboard_commands(subparsers)
        self._add_system_commands(subparsers)
        return parser
    
    def _add_tasks_commands(self, subparsers):
        tasks_parser = subparsers.add_parser("tasks", help="Manage background tasks")
        task_subparsers = tasks_parser.add_subparsers(dest="action")
        add_parser = task_subparsers.add_parser("add", help="Add new task")
        add_parser.add_argument("command", help="Command to run")
        add_parser.add_argument("--name", "-n", help="Task name")
        add_parser.set_defaults(func=self.cmd_tasks_add)
        list_parser = task_subparsers.add_parser("list", help="List all tasks")
        list_parser.set_defaults(func=self.cmd_tasks_list)
        tasks_parser.set_defaults(func=self.cmd_tasks_help)
    
    def _add_clipboard_commands(self, subparsers):
        clip_parser = subparsers.add_parser("clip", help="Manage clipboard")
        clip_subparsers = clip_parser.add_subparsers(dest="action")
        copy_parser = clip_subparsers.add_parser("copy", help="Copy to clipboard")
        copy_parser.add_argument("text", help="Text to copy")
        copy_parser.set_defaults(func=self.cmd_clip_copy)
        paste_parser = clip_subparsers.add_parser("paste", help="Get clipboard content")
        paste_parser.set_defaults(func=self.cmd_clip_paste)
        history_parser = clip_subparsers.add_parser("history", help="View clipboard history")
        history_parser.set_defaults(func=self.cmd_clip_history)
        clip_parser.set_defaults(func=self.cmd_clip_help)
    
    def _add_system_commands(self, subparsers):
        system_parser = subparsers.add_parser("system", help="System information")
        system_subparsers = system_parser.add_subparsers(dest="action")
        health_parser = system_subparsers.add_parser("health", help="System health check")
        health_parser.set_defaults(func=self.cmd_system_health)
        system_parser.set_defaults(func=self.cmd_system_help)
    
    def cmd_tasks_add(self, args) -> int:
        task_id = self.task_manager.add_task(args.command, args.name)
        print(f"✅ Task created: {task_id}")
        return 0
    
    def cmd_tasks_list(self, args) -> int:
        tasks = self.task_manager.list_tasks()
        if not tasks:
            print("No tasks found")
            return 0
        print(f"{'ID':<15} {'Name':<30} {'Status':<12} {'PID':<8}")
        print("-" * 65)
        for task in tasks:
            print(f"{task['id']:<15} {task['name']:<30} {task['status']:<12} {task['pid']:<8}")
        return 0
    
    def cmd_tasks_help(self, args) -> int:
        print("\nTask Management:\n  antigravity tasks add \"npm start\"\n  antigravity tasks list\n")
        return 0
    
    def cmd_clip_copy(self, args) -> int:
        self.clipboard_manager.copy(args.text)
        print(f"📋 Copied: {args.text[:50]}..." if len(args.text) > 50 else f"📋 Copied: {args.text}")
        return 0
    
    def cmd_clip_paste(self, args) -> int:
        content = self.clipboard_manager.paste()
        print(content, end="")
        return 0
    
    def cmd_clip_history(self, args) -> int:
        history = self.clipboard_manager.history(10)
        if not history:
            print("No clipboard history")
            return 0
        for i, item in enumerate(history, 1):
            print(f"{i}. {item.strip()}")
        return 0
    
    def cmd_clip_help(self, args) -> int:
        print("\nClipboard Management:\n  antigravity clip copy <text>\n  antigravity clip paste\n  antigravity clip history\n")
        return 0
    
    def cmd_system_health(self, args) -> int:
        health = self.system_info.get_health()
        print(f"\n📊 System Health\n")
        print(f"Storage: {health['storage']['used_gb']}GB / {health['storage']['total_gb']}GB ({health['storage']['percent_used']}%)")
        print(f"Memory: {health['memory'].get('used_mb', 'N/A')}MB\n")
        return 0
    
    def cmd_system_help(self, args) -> int:
        print("\nSystem Information:\n  antigravity system health\n")
        return 0

def main(args=None):
    cli = AntiGravityCLI()
    return cli.run(args)
