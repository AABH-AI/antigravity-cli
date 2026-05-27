"""AntiGravity AI - Main CLI Interface"""

import sys
import argparse
from pathlib import Path

from .ai_engine import GeminiAI
from .github_deployer import GitHubDeployer
from .project_gen import ProjectGenerator
from .task_engine import TaskEngine

class AntiGravityAI:
    """AI-Powered Development Platform"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".antigravity"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.ai = GeminiAI(api_key=self._get_api_key('GEMINI'))
        self.github = GitHubDeployer(
            token=self._get_api_key('GITHUB_TOKEN'),
            username=self._get_api_key('GITHUB_USERNAME')
        )
        self.projects = ProjectGenerator(self.config_dir)
        self.tasks = TaskEngine(self.config_dir)
    
    def _get_api_key(self, env_var: str) -> str:
        """Get API key from environment or config"""
        import os
        return os.getenv(env_var, "")
    
    def run(self, args=None):
        """Main entry point"""
        parser = self._create_parser()
        parsed_args = parser.parse_args(args)
        
        if hasattr(parsed_args, 'func'):
            return parsed_args.func(parsed_args)
        parser.print_help()
        return 0
    
    def _create_parser(self):
        """Create CLI parser"""
        parser = argparse.ArgumentParser(
            prog="antigravity",
            description="🚀 AntiGravity AI - AI-Powered Development Platform",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  antigravity ai setup --gemini YOUR_KEY --github YOUR_TOKEN
  antigravity ai task "Build a todo app in Python"
  antigravity project create myapp python
  antigravity code generate "Hello world app"
  antigravity deploy myapp
  antigravity review mycode.py
            """
        )
        
        parser.add_argument("--version", action="version", version="antigravity 2.0.0")
        
        subparsers = parser.add_subparsers(title="commands", dest="command")
        
        # AI commands
        self._add_ai_commands(subparsers)
        
        # Project commands
        self._add_project_commands(subparsers)
        
        # Code commands
        self._add_code_commands(subparsers)
        
        # Deploy commands
        self._add_deploy_commands(subparsers)
        
        # Task commands
        self._add_task_commands(subparsers)
        
        return parser
    
    def _add_ai_commands(self, subparsers):
        """Add AI commands"""
        ai_parser = subparsers.add_parser(
            "ai",
            help="AI engine commands"
        )
        ai_sub = ai_parser.add_subparsers(dest="action")
        
        # Setup
        setup = ai_sub.add_parser("setup", help="Setup AI credentials")
        setup.add_argument("--gemini", help="Gemini API key")
        setup.add_argument("--github", help="GitHub token")
        setup.add_argument("--username", help="GitHub username")
        setup.set_defaults(func=self.cmd_ai_setup)
        
        # Status
        status = ai_sub.add_parser("status", help="Check AI status")
        status.set_defaults(func=self.cmd_ai_status)
        
        # Task
        task = ai_sub.add_parser("task", help="Create AI task")
        task.add_argument("description", help="Task description")
        task.add_argument("--language", default="python", help="Language")
        task.set_defaults(func=self.cmd_ai_task)
        
        ai_parser.set_defaults(func=self.cmd_ai_help)
    
    def _add_project_commands(self, subparsers):
        """Add project commands"""
        proj_parser = subparsers.add_parser(
            "project",
            help="Project management"
        )
        proj_sub = proj_parser.add_subparsers(dest="action")
        
        # Create
        create = proj_sub.add_parser("create", help="Create new project")
        create.add_argument("name", help="Project name")
        create.add_argument("language", help="Programming language")
        create.add_argument("--description", help="Project description")
        create.set_defaults(func=self.cmd_project_create)
        
        # List
        list_cmd = proj_sub.add_parser("list", help="List projects")
        list_cmd.set_defaults(func=self.cmd_project_list)
        
        # Info
        info = proj_sub.add_parser("info", help="Project info")
        info.add_argument("name", help="Project name")
        info.set_defaults(func=self.cmd_project_info)
        
        proj_parser.set_defaults(func=self.cmd_project_help)
    
    def _add_code_commands(self, subparsers):
        """Add code generation commands"""
        code_parser = subparsers.add_parser(
            "code",
            help="Code generation"
        )
        code_sub = code_parser.add_subparsers(dest="action")
        
        # Generate
        gen = code_sub.add_parser("generate", help="Generate code")
        gen.add_argument("description", help="What to build")
        gen.add_argument("--language", default="python", help="Language")
        gen.add_argument("--output", help="Save to file")
        gen.set_defaults(func=self.cmd_code_generate)
        
        # Build app
        build = code_sub.add_parser("build", help="Build application")
        build.add_argument("description", help="App description")
        build.add_argument("--name", required=True, help="App name")
        build.set_defaults(func=self.cmd_code_build)
        
        # Fix
        fix = code_sub.add_parser("fix", help="Fix code")
        fix.add_argument("file", help="Code file")
        fix.add_argument("--error", help="Error message")
        fix.set_defaults(func=self.cmd_code_fix)
        
        # Review
        review = code_sub.add_parser("review", help="Review code")
        review.add_argument("file", help="Code file")
        review.set_defaults(func=self.cmd_code_review)
        
        code_parser.set_defaults(func=self.cmd_code_help)
    
    def _add_deploy_commands(self, subparsers):
        """Add deployment commands"""
        deploy_parser = subparsers.add_parser(
            "deploy",
            help="Deploy to GitHub"
        )
        deploy_sub = deploy_parser.add_subparsers(dest="action")
        
        # Create repo
        repo = deploy_sub.add_parser("repo", help="Create GitHub repo")
        repo.add_argument("name", help="Repository name")
        repo.add_argument("--description", help="Description")
        repo.add_argument("--private", action="store_true", help="Private repo")
        repo.set_defaults(func=self.cmd_deploy_repo)
        
        # Push
        push = deploy_sub.add_parser("push", help="Push code")
        push.add_argument("repo", help="Repository name")
        push.add_argument("--message", default="Initial commit", help="Commit message")
        push.set_defaults(func=self.cmd_deploy_push)
        
        # Setup CI/CD
        cicd = deploy_sub.add_parser("cicd", help="Setup GitHub Actions")
        cicd.add_argument("repo", help="Repository name")
        cicd.set_defaults(func=self.cmd_deploy_cicd)
        
        deploy_parser.set_defaults(func=self.cmd_deploy_help)
    
    def _add_task_commands(self, subparsers):
        """Add task management commands"""
        task_parser = subparsers.add_parser(
            "task",
            help="Task management"
        )
        task_sub = task_parser.add_subparsers(dest="action")
        
        # New
        new = task_sub.add_parser("new", help="Create task")
        new.add_argument("description", help="Task description")
        new.add_argument("--type", default="general", help="Task type")
        new.set_defaults(func=self.cmd_task_new)
        
        # List
        list_cmd = task_sub.add_parser("list", help="List tasks")
        list_cmd.add_argument("--status", help="Filter by status")
        list_cmd.set_defaults(func=self.cmd_task_list)
        
        # Run
        run = task_sub.add_parser("run", help="Run task")
        run.add_argument("task_id", help="Task ID")
        run.set_defaults(func=self.cmd_task_run)
        
        task_parser.set_defaults(func=self.cmd_task_help)
    
    # AI Commands
    def cmd_ai_setup(self, args):
        """Setup AI credentials"""
        print("\n🔑 AntiGravity AI Setup\n")
        if args.gemini:
            print(f"✅ Gemini API configured")
        if args.github:
            print(f"✅ GitHub token configured")
        if args.username:
            print(f"✅ GitHub username: {args.username}")
        print()
        return 0
    
    def cmd_ai_status(self, args):
        """Check AI status"""
        print("\n📊 AntiGravity AI Status\n")
        print(f"Gemini API: {'✅ Configured' if self.ai.is_configured() else '❌ Not configured'}")
        print(f"GitHub: {'✅ Configured' if self.github.is_configured() else '❌ Not configured'}")
        print()
        return 0
    
    def cmd_ai_task(self, args):
        """Create AI task"""
        task_id = self.tasks.create_task(args.description, "ai_generated")
        self.tasks.execute_task(task_id)
        return 0
    
    def cmd_ai_help(self, args):
        """Show AI help"""
        print("""\nAI Commands:
  antigravity ai setup --gemini KEY --github TOKEN --username USER
  antigravity ai status
  antigravity ai task "Build a todo app in Python"
        """)
        return 0
    
    # Project Commands
    def cmd_project_create(self, args):
        """Create project"""
        result = self.projects.create_project(
            args.name, 
            args.language,
            args.description or ""
        )
        return 0
    
    def cmd_project_list(self, args):
        """List projects"""
        projects = self.projects.list_projects()
        print(f"\n📂 Your Projects ({len(projects)})\n")
        for proj in projects:
            print(f"  • {proj}")
        print()
        return 0
    
    def cmd_project_info(self, args):
        """Show project info"""
        info = self.projects.get_project_info(args.name)
        print(f"\n📊 Project: {args.name}\n")
        for key, val in info.items():
            if key != 'files':
                print(f"  {key}: {val}")
        print()
        return 0
    
    def cmd_project_help(self, args):
        """Show project help"""
        print("""\nProject Commands:
  antigravity project create NAME LANGUAGE [--description DESC]
  antigravity project list
  antigravity project info NAME
        """)
        return 0
    
    # Code Commands
    def cmd_code_generate(self, args):
        """Generate code"""
        print(f"\n🤖 Generating {args.language} code...\n")
        code = self.ai.generate_code(args.description, args.language)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(code)
            print(f"✅ Code saved to {args.output}\n")
        else:
            print(code)
            print()
        return 0
    
    def cmd_code_build(self, args):
        """Build application"""
        print(f"\n🏗️  Building application: {args.name}\n")
        result = self.ai.build_app(args.description)
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}\n")
        return 0
    
    def cmd_code_fix(self, args):
        """Fix code"""
        print(f"\n🔧 Analyzing code...\n")
        try:
            with open(args.file) as f:
                code = f.read()
            fixed = self.ai.fix_code(code, args.error or "")
            print(fixed)
            print()
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}\n")
            return 1
        return 0
    
    def cmd_code_review(self, args):
        """Review code"""
        print(f"\n👀 Reviewing code...\n")
        try:
            with open(args.file) as f:
                code = f.read()
            review = self.ai.review_code(code)
            print(review)
            print()
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}\n")
            return 1
        return 0
    
    def cmd_code_help(self, args):
        """Show code help"""
        print("""\nCode Commands:
  antigravity code generate "Description" [--language LANG] [--output FILE]
  antigravity code build "App Description" --name APP_NAME
  antigravity code fix FILE [--error ERROR_MSG]
  antigravity code review FILE
        """)
        return 0
    
    # Deploy Commands
    def cmd_deploy_repo(self, args):
        """Create repo"""
        result = self.github.create_repo(args.name, args.description or "", args.private)
        print(f"\n✅ Repository created\n")
        for key, val in result.items():
            print(f"  {key}: {val}")
        print()
        return 0
    
    def cmd_deploy_push(self, args):
        """Push code"""
        print(f"\n📤 Pushing to {args.repo}...\n")
        success = self.github.push_code(args.repo, {}, args.message)
        if success:
            print(f"✅ Code pushed successfully\n")
        return 0
    
    def cmd_deploy_cicd(self, args):
        """Setup CI/CD"""
        success = self.github.setup_ci_cd(args.repo)
        if success:
            print(f"\n✅ GitHub Actions configured\n")
        return 0
    
    def cmd_deploy_help(self, args):
        """Show deploy help"""
        print("""\nDeploy Commands:
  antigravity deploy repo NAME [--description DESC] [--private]
  antigravity deploy push REPO [--message MSG]
  antigravity deploy cicd REPO
        """)
        return 0
    
    # Task Commands
    def cmd_task_new(self, args):
        """Create task"""
        task_id = self.tasks.create_task(args.description, args.type)
        return 0
    
    def cmd_task_list(self, args):
        """List tasks"""
        tasks = self.tasks.list_tasks(args.status)
        print(f"\n📋 Tasks ({len(tasks)})\n")
        for task_id, task in self.tasks.tasks.items():
            print(f"  {task_id}: {task['description']}")
            print(f"    Status: {task['status']}\n")
        return 0
    
    def cmd_task_run(self, args):
        """Run task"""
        result = self.tasks.execute_task(args.task_id)
        if 'error' not in result:
            self.tasks.complete_task(args.task_id, "Completed")
        return 0
    
    def cmd_task_help(self, args):
        """Show task help"""
        print("""\nTask Commands:
  antigravity task new "Description" [--type TYPE]
  antigravity task list [--status STATUS]
  antigravity task run TASK_ID
        """)
        return 0


def main(args=None):
    """Entry point"""
    cli = AntiGravityAI()
    return cli.run(args)
