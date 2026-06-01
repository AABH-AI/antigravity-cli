"""Project Generator and Manager"""

import os
from pathlib import Path
from typing import Dict, List


class ProjectGenerator:
    """Generate and manage project scaffolding"""

    SUPPORTED_LANGUAGES = ["python", "javascript", "bash"]

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.projects_dir = base_path / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    def create_project(self, name: str, language: str,
                       description: str = "") -> Dict:
        """Scaffold a new project with boilerplate files"""
        language = language.lower()
        if language not in self.SUPPORTED_LANGUAGES:
            print(f"⚠️  Unknown language '{language}'. Supported: {', '.join(self.SUPPORTED_LANGUAGES)}")
            print("   Continuing with generic scaffold.\n")

        project_path = self.projects_dir / name
        if project_path.exists():
            print(f"⚠️  Project '{name}' already exists at {project_path}")
            print("   Use a different name or delete the existing project.\n")
            return {"error": f"Project '{name}' already exists"}

        project_path.mkdir(parents=True)
        print(f"\n📁 Creating project: {name}")
        print(f"   Language   : {language}")
        print(f"   Location   : {project_path}\n")

        structure = self._scaffold(language, name, description)
        for rel_path, content in structure.items():
            full_path = project_path / rel_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            print(f"  ✅ {rel_path}")

        print(f"\n🎉 Project ready. Run: cd {project_path}\n")
        return {
            "name": name,
            "path": str(project_path),
            "language": language,
            "files": list(structure.keys()),
        }

    def _scaffold(self, language: str, name: str, description: str) -> Dict[str, str]:
        desc = description or f"A {language} project"

        if language == "python":
            return {
                "main.py": f'''#!/usr/bin/env python3
"""{description or name}"""


def main() -> None:
    print("Hello from {name}!")


if __name__ == "__main__":
    main()
''',
                "requirements.txt": "# Add your dependencies here\n# Example: requests>=2.31\n",
                ".gitignore": "__pycache__/\n*.pyc\n*.egg-info/\n.venv/\ndist/\nbuild/\n",
                "README.md": f"# {name}\n\n{desc}\n\n## Setup\n\n```bash\npip install -r requirements.txt\npython main.py\n```\n",
            }

        elif language == "javascript":
            return {
                "index.js": f'''// {description or name}

function main() {{
    console.log("Hello from {name}!");
}}

main();
''',
                "package.json": f'''{{\n  "name": "{name.lower()}",\n  "version": "1.0.0",\n  "description": "{desc}",\n  "main": "index.js",\n  "scripts": {{\n    "start": "node index.js"\n  }}\n}}\n''',
                ".gitignore": "node_modules/\n.env\n",
                "README.md": f"# {name}\n\n{desc}\n\n## Setup\n\n```bash\nnpm install\nnpm start\n```\n",
            }

        elif language == "bash":
            return {
                "main.sh": f'''#!/usr/bin/env bash
# {description or name}
set -euo pipefail

main() {{
    echo "Hello from {name}!"
}}

main "$@"
''',
                "README.md": f"# {name}\n\n{desc}\n\n## Setup\n\n```bash\nchmod +x main.sh\n./main.sh\n```\n",
                ".gitignore": "*.log\n",
            }

        else:
            return {
                "README.md": f"# {name}\n\n{desc}\n",
            }

    def list_projects(self) -> List[str]:
        return sorted(d.name for d in self.projects_dir.iterdir() if d.is_dir())

    def get_project_info(self, name: str) -> Dict:
        project_path = self.projects_dir / name
        if not project_path.exists():
            return {"error": f"Project '{name}' not found. Run: antigravity project list"}

        all_files = [f for f in project_path.rglob("*") if f.is_file()]
        return {
            "name": name,
            "path": str(project_path),
            "file_count": len(all_files),
            "files": [str(f.relative_to(project_path)) for f in all_files],
        }
