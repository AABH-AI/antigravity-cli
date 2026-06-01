"""AntiGravity AI - Main CLI Interface"""

import sys
import os
import json
import argparse
from pathlib import Path

from .ai_engine import GeminiAI, GeminiAIError
from .github_deployer import GitHubDeployer, GitHubError
from .project_gen import ProjectGenerator
from .task_engine import TaskEngine
from .termux_utils import TermuxUtils


CONFIG_FILE = Path.home() / ".antigravity" / "config.json"


def _load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_config(data: dict) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2))


def _get_key(cfg: dict, env_var: str, cfg_key: str) -> str:
    """Precedence: environment variable > saved config"""
    return os.environ.get(env_var, "") or cfg.get(cfg_key, "")


class AntiGravityAI:
    """AI-Powered Development Platform"""

    def __init__(self):
        self.config_dir = Path.home() / ".antigravity"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        cfg = _load_config()
        gemini_key = _get_key(cfg, "GEMINI_API_KEY", "gemini_key")
        github_token = _get_key(cfg, "GITHUB_TOKEN", "github_token")
        github_user = _get_key(cfg, "GITHUB_USERNAME", "github_username")

        self.ai = GeminiAI(api_key=gemini_key)
        self.github = GitHubDeployer(token=github_token, username=github_user)
        self.projects = ProjectGenerator(self.config_dir)
        self.tasks = TaskEngine(self.config_dir)

    # ------------------------------------------------------------------ #
    # Entry point                                                           #
    # ------------------------------------------------------------------ #

    def run(self, args=None):
        parser = self._build_parser()
        parsed = parser.parse_args(args)

        if hasattr(parsed, "func"):
            try:
                return parsed.func(parsed) or 0
            except GeminiAIError as e:
                print(f"\n❌ AI Error: {e}\n", file=sys.stderr)
                return 1
            except GitHubError as e:
                print(f"\n❌ GitHub Error: {e}\n", file=sys.stderr)
                return 1
            except KeyboardInterrupt:
                print("\n\n⚡ Cancelled.\n")
                return 0
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}\n", file=sys.stderr)
                return 1

        parser.print_help()
        return 0

    # ------------------------------------------------------------------ #
    # Parser                                                                #
    # ------------------------------------------------------------------ #

    def _build_parser(self):
        parser = argparse.ArgumentParser(
            prog="antigravity",
            description="🚀 AntiGravity AI - AI-Powered Dev Platform for Termux",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  antigravity ai setup --gemini YOUR_KEY --github TOKEN --username YOU
  antigravity ai status
  antigravity ai task "Build a Flask todo API"
  antigravity code generate "sort a list" --language python
  antigravity code build "weather app" --name weatherapp
  antigravity code review myfile.py
  antigravity code fix myfile.py --error "NameError: x not defined"
  antigravity project create myapp python
  antigravity deploy repo myapp --description "My app"
  antigravity deploy push myapp
  antigravity deploy cicd myapp
  antigravity task new "Add login feature"
  antigravity task list
  antigravity task run task_1
            """,
        )
        parser.add_argument("--version", action="version", version="AntiGravity AI 2.0.0")

        subs = parser.add_subparsers(title="commands", dest="command")
        self._add_ai_commands(subs)
        self._add_code_commands(subs)
        self._add_project_commands(subs)
        self._add_deploy_commands(subs)
        self._add_task_commands(subs)
        return parser

    # ------------------------------------------------------------------ #
    # Sub-command registration                                              #
    # ------------------------------------------------------------------ #

    def _add_ai_commands(self, subs):
        p = subs.add_parser("ai", help="AI engine & setup")
        s = p.add_subparsers(dest="action")

        setup = s.add_parser("setup", help="Save API keys locally")
        setup.add_argument("--gemini", metavar="KEY", help="Gemini API key")
        setup.add_argument("--github", metavar="TOKEN", help="GitHub personal access token")
        setup.add_argument("--username", metavar="USER", help="GitHub username")
        setup.set_defaults(func=self._cmd_ai_setup)

        s.add_parser("status", help="Show config status").set_defaults(func=self._cmd_ai_status)

        task = s.add_parser("task", help="Ask AI to build something end-to-end")
        task.add_argument("description", help="What to build (natural language)")
        task.add_argument("--language", default="python", help="Language (default: python)")
        task.add_argument("--push", action="store_true", help="Auto-push result to GitHub")
        task.set_defaults(func=self._cmd_ai_task)

        p.set_defaults(func=lambda _: p.print_help())

    def _add_code_commands(self, subs):
        p = subs.add_parser("code", help="Code generation & review")
        s = p.add_subparsers(dest="action")

        gen = s.add_parser("generate", help="Generate code from description")
        gen.add_argument("description", help="What to build")
        gen.add_argument("--language", default="python")
        gen.add_argument("--output", metavar="FILE", help="Save to file")
        gen.set_defaults(func=self._cmd_code_generate)

        build = s.add_parser("build", help="Build a full app (multi-file)")
        build.add_argument("description", help="App description")
        build.add_argument("--name", required=True, help="App/folder name")
        build.add_argument("--push", action="store_true", help="Push to GitHub after build")
        build.set_defaults(func=self._cmd_code_build)

        fix = s.add_parser("fix", help="Fix errors in a file")
        fix.add_argument("file")
        fix.add_argument("--error", default="", help="Error message to guide the fix")
        fix.add_argument("--inplace", action="store_true", help="Overwrite original file")
        fix.set_defaults(func=self._cmd_code_fix)

        review = s.add_parser("review", help="AI code review")
        review.add_argument("file")
        review.set_defaults(func=self._cmd_code_review)

        explain = s.add_parser("explain", help="Explain what code does")
        explain.add_argument("file")
        explain.set_defaults(func=self._cmd_code_explain)

        p.set_defaults(func=lambda _: p.print_help())

    def _add_project_commands(self, subs):
        p = subs.add_parser("project", help="Project management")
        s = p.add_subparsers(dest="action")

        create = s.add_parser("create", help="Scaffold a new project")
        create.add_argument("name")
        create.add_argument("language", choices=["python", "javascript", "bash"])
        create.add_argument("--description", default="")
        create.set_defaults(func=self._cmd_project_create)

        s.add_parser("list", help="List all projects").set_defaults(func=self._cmd_project_list)

        info = s.add_parser("info", help="Show project details")
        info.add_argument("name")
        info.set_defaults(func=self._cmd_project_info)

        p.set_defaults(func=lambda _: p.print_help())

    def _add_deploy_commands(self, subs):
        p = subs.add_parser("deploy", help="GitHub deployment")
        s = p.add_subparsers(dest="action")

        repo = s.add_parser("repo", help="Create GitHub repository")
        repo.add_argument("name", help="Repo name")
        repo.add_argument("--description", default="")
        repo.add_argument("--private", action="store_true")
        repo.set_defaults(func=self._cmd_deploy_repo)

        push = s.add_parser("push", help="Push project files to GitHub")
        push.add_argument("name", help="Project / repo name")
        push.add_argument("--message", default="Update from AntiGravity AI")
        push.set_defaults(func=self._cmd_deploy_push)

        cicd = s.add_parser("cicd", help="Add GitHub Actions to repo")
        cicd.add_argument("name", help="Repo name")
        cicd.add_argument("--language", default="python")
        cicd.set_defaults(func=self._cmd_deploy_cicd)

        p.set_defaults(func=lambda _: p.print_help())

    def _add_task_commands(self, subs):
        p = subs.add_parser("task", help="Task tracking")
        s = p.add_subparsers(dest="action")

        new = s.add_parser("new", help="Create a new task")
        new.add_argument("description")
        new.add_argument("--type", default="general")
        new.set_defaults(func=self._cmd_task_new)

        lst = s.add_parser("list", help="List tasks")
        lst.add_argument("--status", help="Filter: pending/running/completed/failed")
        lst.set_defaults(func=self._cmd_task_list)

        run = s.add_parser("run", help="Execute a task with AI")
        run.add_argument("task_id")
        run.set_defaults(func=self._cmd_task_run)

        p.set_defaults(func=lambda _: p.print_help())

    # ------------------------------------------------------------------ #
    # AI command handlers                                                   #
    # ------------------------------------------------------------------ #

    def _cmd_ai_setup(self, args):
        cfg = _load_config()
        changed = False
        if args.gemini:
            cfg["gemini_key"] = args.gemini
            print("  ✅ Gemini API key saved")
            changed = True
        if args.github:
            cfg["github_token"] = args.github
            print("  ✅ GitHub token saved")
            changed = True
        if args.username:
            cfg["github_username"] = args.username
            print(f"  ✅ GitHub username saved: {args.username}")
            changed = True
        if changed:
            _save_config(cfg)
            print(f"\n  Config stored in: {CONFIG_FILE}\n")
            # Re-init with new keys
            self.__init__()
        else:
            print("  ℹ️  Nothing to save. Pass --gemini, --github, and/or --username.\n")

    def _cmd_ai_status(self, args):
        print("\n📊 AntiGravity AI Status\n")
        gemini_ok = self.ai.is_configured()
        github_ok = self.github.is_configured()
        termux = TermuxUtils.is_termux()

        print(f"  Gemini API : {'✅ Configured' if gemini_ok else '❌ Not set  → run: antigravity ai setup --gemini KEY'}")
        print(f"  GitHub     : {'✅ Configured' if github_ok else '❌ Not set  → run: antigravity ai setup --github TOKEN --username USER'}")
        print(f"  Environment: {'📱 Termux' if termux else '🖥  Desktop/Linux'}")

        if gemini_ok:
            print("\n  🔬 Testing Gemini connection...")
            try:
                result = self.ai._call_api("Reply with exactly: OK", max_tokens=5)
                print(f"  Gemini ping : ✅ {result.strip()}")
            except GeminiAIError as e:
                print(f"  Gemini ping : ❌ {e}")
        print()

    def _cmd_ai_task(self, args):
        """End-to-end: generate app → save files → optionally push to GitHub"""
        print(f"\n🚀 AntiGravity AI Task\n  Task: {args.description}\n")

        task_id = self.tasks.create_task(args.description, "ai_generated")

        # Generate full app
        result = self.ai.build_app(args.description)
        files = result.get("files", {})

        if not files:
            print("❌ AI returned no files.\n")
            return 1

        # Save files locally under ~/.antigravity/projects/<slugified-name>
        slug = args.description[:40].lower().replace(" ", "-").replace("/", "-")
        project_dir = self.config_dir / "projects" / slug
        project_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n📁 Saving files to: {project_dir}\n")
        for filepath, content in files.items():
            dest = project_dir / filepath
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)
            print(f"  ✅ {filepath}")

        self.tasks.complete_task(task_id, "Files generated")

        if args.push:
            if not self.github.is_configured():
                print("\n⚠️  GitHub not configured, skipping push.\n")
            else:
                repo_name = slug[:40]
                if not self.github.repo_exists(repo_name):
                    self.github.create_repo(repo_name, args.description)
                self.github.push_files(repo_name, files, f"feat: {args.description[:72]}")

        print(f"\n🎉 Done! Project at: {project_dir}\n")

    # ------------------------------------------------------------------ #
    # Code command handlers                                                 #
    # ------------------------------------------------------------------ #

    def _cmd_code_generate(self, args):
        print(f"\n🤖 Generating {args.language} code for: \"{args.description}\"\n")
        code = self.ai.generate_code(args.description, args.language)

        if args.output:
            Path(args.output).write_text(code)
            print(f"\n✅ Saved to: {args.output}\n")
        else:
            print("\n" + code + "\n")

    def _cmd_code_build(self, args):
        print(f"\n🏗️  Building app: {args.name}\n  Description: {args.description}\n")
        result = self.ai.build_app(args.description)

        if result["status"] == "partial":
            print(f"  ⚠️  {result.get('warning', '')}")

        files = result.get("files", {})
        project_dir = Path(args.name)
        project_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n📁 Writing files to ./{args.name}/\n")
        for filepath, content in files.items():
            dest = project_dir / filepath
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)
            print(f"  ✅ {filepath}")

        if args.push and self.github.is_configured():
            repo_name = args.name
            if not self.github.repo_exists(repo_name):
                self.github.create_repo(repo_name, args.description)
            self.github.push_files(repo_name, files, f"feat: initial {args.name} build")

        print(f"\n🎉 App built in ./{args.name}/\n")

    def _cmd_code_fix(self, args):
        path = Path(args.file)
        if not path.exists():
            print(f"\n❌ File not found: {args.file}\n", file=sys.stderr)
            return 1

        print(f"\n🔧 Fixing {args.file}...\n")
        code = path.read_text()
        fixed = self.ai.fix_code(code, args.error)

        if args.inplace:
            path.write_text(fixed)
            print(f"  ✅ File updated in place: {args.file}\n")
        else:
            print("\n" + fixed + "\n")

    def _cmd_code_review(self, args):
        path = Path(args.file)
        if not path.exists():
            print(f"\n❌ File not found: {args.file}\n", file=sys.stderr)
            return 1

        print(f"\n👀 Reviewing {args.file}...\n")
        code = path.read_text()
        review = self.ai.review_code(code)
        print("\n" + review + "\n")

    def _cmd_code_explain(self, args):
        path = Path(args.file)
        if not path.exists():
            print(f"\n❌ File not found: {args.file}\n", file=sys.stderr)
            return 1

        print(f"\n📖 Explaining {args.file}...\n")
        code = path.read_text()
        explanation = self.ai.explain_code(code)
        print("\n" + explanation + "\n")

    # ------------------------------------------------------------------ #
    # Project command handlers                                              #
    # ------------------------------------------------------------------ #

    def _cmd_project_create(self, args):
        self.projects.create_project(args.name, args.language, args.description)

    def _cmd_project_list(self, args):
        projects = self.projects.list_projects()
        print(f"\n📂 Your Projects ({len(projects)})\n")
        if not projects:
            print("  (none yet — run: antigravity project create NAME LANGUAGE)\n")
        for p in projects:
            print(f"  • {p}")
        print()

    def _cmd_project_info(self, args):
        info = self.projects.get_project_info(args.name)
        if "error" in info:
            print(f"\n❌ {info['error']}\n", file=sys.stderr)
            return 1
        print(f"\n📊 Project: {args.name}\n")
        for k, v in info.items():
            if k != "files":
                print(f"  {k}: {v}")
        print()

    # ------------------------------------------------------------------ #
    # Deploy command handlers                                               #
    # ------------------------------------------------------------------ #

    def _cmd_deploy_repo(self, args):
        result = self.github.create_repo(args.name, args.description, args.private)
        print(f"  URL: {result['url']}\n")

    def _cmd_deploy_push(self, args):
        info = self.projects.get_project_info(args.name)
        if "error" in info:
            print(f"\n❌ {info['error']}\n", file=sys.stderr)
            return 1

        project_path = Path(info["path"])
        files: dict = {}
        for f in project_path.rglob("*"):
            if f.is_file() and ".git" not in f.parts:
                try:
                    rel = str(f.relative_to(project_path))
                    files[rel] = f.read_text(errors="replace")
                except Exception:
                    pass

        if not files:
            print(f"\n❌ No files found in project '{args.name}'\n", file=sys.stderr)
            return 1

        if not self.github.repo_exists(args.name):
            self.github.create_repo(args.name)

        self.github.push_files(args.name, files, args.message)

    def _cmd_deploy_cicd(self, args):
        self.github.setup_ci_cd(args.name, args.language)

    # ------------------------------------------------------------------ #
    # Task command handlers                                                 #
    # ------------------------------------------------------------------ #

    def _cmd_task_new(self, args):
        self.tasks.create_task(args.description, args.type)

    def _cmd_task_list(self, args):
        tasks = self.tasks.list_tasks(args.status)
        print(f"\n📋 Tasks ({len(tasks)})\n")
        if not tasks:
            print("  (none yet — run: antigravity task new \"description\")\n")
            return
        for t in tasks:
            print(f"  [{t['id']}] {t['description']}")
            print(f"       Status: {t['status']}  Type: {t.get('type', '-')}")
            print()

    def _cmd_task_run(self, args):
        result = self.tasks.execute_task(args.task_id)
        if "error" in result:
            print(f"\n❌ {result['error']}\n", file=sys.stderr)
            return 1

        # Use AI to actually do the task
        task = self.tasks.get_task(args.task_id)
        desc = task.get("description", "")
        if desc and self.ai.is_configured():
            print(f"\n🤖 Asking AI to handle: {desc}\n")
            code = self.ai.generate_code(desc)
            print(code)
            self.tasks.complete_task(args.task_id, "AI-generated")
        else:
            self.tasks.complete_task(args.task_id, "Marked done")


def main(args=None):
    cli = AntiGravityAI()
    sys.exit(cli.run(args))
