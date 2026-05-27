"""Main CLI Interface for AntiGravity"""

import sys
import argparse
from pathlib import Path

from .google_auth import GoogleAuthManager
from .google_drive import GoogleDriveManager
from .termux_utils import TermuxUtils


class AntiGravityCLI:
    """AntiGravity CLI with Google Integration"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".antigravity"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.auth = GoogleAuthManager(self.config_dir)
        self.drive = GoogleDriveManager(self.config_dir, self.auth)
    
    def run(self, args=None):
        """Main entry point"""
        parser = self._create_parser()
        parsed_args = parser.parse_args(args)
        
        if hasattr(parsed_args, 'func'):
            return parsed_args.func(parsed_args)
        parser.print_help()
        return 0
    
    def _create_parser(self):
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            prog="antigravity",
            description="🚀 AntiGravity CLI - Termux + Google Integration",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  antigravity google setup --id YOUR_CLIENT_ID --secret YOUR_SECRET
  antigravity google auth
  antigravity google list
  antigravity google upload file.txt
  antigravity drive sync ~/Documents
  antigravity info
            """
        )
        
        parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
        
        subparsers = parser.add_subparsers(title="commands", dest="command")
        
        # Google authentication commands
        self._add_google_commands(subparsers)
        
        # Drive commands
        self._add_drive_commands(subparsers)
        
        # System info commands
        self._add_info_commands(subparsers)
        
        return parser
    
    def _add_google_commands(self, subparsers):
        """Add Google authentication commands"""
        google_parser = subparsers.add_parser(
            "google",
            help="Google OAuth2 setup and management"
        )
        google_sub = google_parser.add_subparsers(dest="action")
        
        # Setup
        setup = google_sub.add_parser("setup", help="Configure Google OAuth2")
        setup.add_argument("--id", required=True, help="Google Client ID")
        setup.add_argument("--secret", required=True, help="Google Client Secret")
        setup.set_defaults(func=self.cmd_google_setup)
        
        # Auth
        auth = google_sub.add_parser("auth", help="Authenticate with Google")
        auth.add_argument("--code", help="OAuth2 authorization code")
        auth.set_defaults(func=self.cmd_google_auth)
        
        # Status
        status = google_sub.add_parser("status", help="Check authentication status")
        status.set_defaults(func=self.cmd_google_status)
        
        # List files
        list_cmd = google_sub.add_parser("list", help="List Google Drive files")
        list_cmd.set_defaults(func=self.cmd_google_list)
        
        # Upload
        upload = google_sub.add_parser("upload", help="Upload file to Google Drive")
        upload.add_argument("file", help="Local file to upload")
        upload.add_argument("--path", default="/", help="Drive destination path")
        upload.set_defaults(func=self.cmd_google_upload)
        
        # Download
        download = google_sub.add_parser("download", help="Download from Google Drive")
        download.add_argument("file_id", help="File ID to download")
        download.add_argument("--output", required=True, help="Local output path")
        download.set_defaults(func=self.cmd_google_download)
        
        google_parser.set_defaults(func=self.cmd_google_help)
    
    def _add_drive_commands(self, subparsers):
        """Add Google Drive commands"""
        drive_parser = subparsers.add_parser(
            "drive",
            help="Google Drive operations"
        )
        drive_sub = drive_parser.add_subparsers(dest="action")
        
        # Sync
        sync = drive_sub.add_parser("sync", help="Sync folder with Google Drive")
        sync.add_argument("folder", help="Local folder to sync")
        sync.add_argument("--path", default="/", help="Drive destination")
        sync.set_defaults(func=self.cmd_drive_sync)
        
        # Quota
        quota = drive_sub.add_parser("quota", help="Check storage quota")
        quota.set_defaults(func=self.cmd_drive_quota)
        
        # Create folder
        mkdir = drive_sub.add_parser("mkdir", help="Create folder on Drive")
        mkdir.add_argument("name", help="Folder name")
        mkdir.add_argument("--parent", default="root", help="Parent folder ID")
        mkdir.set_defaults(func=self.cmd_drive_mkdir)
        
        drive_parser.set_defaults(func=self.cmd_drive_help)
    
    def _add_info_commands(self, subparsers):
        """Add system info commands"""
        info_parser = subparsers.add_parser(
            "info",
            help="System and environment info"
        )
        info_sub = info_parser.add_subparsers(dest="action")
        
        # Device info
        device = info_sub.add_parser("device", help="Device information")
        device.set_defaults(func=self.cmd_info_device)
        
        # Storage
        storage = info_sub.add_parser("storage", help="Storage paths")
        storage.set_defaults(func=self.cmd_info_storage)
        
        info_parser.set_defaults(func=self.cmd_info_device)
    
    # Google commands
    def cmd_google_setup(self, args):
        """Setup Google OAuth2"""
        print("\n🔐 Setting up Google OAuth2...\n")
        success = self.auth.setup_oauth(args.id, args.secret)
        print(f"   Next: antigravity google auth\n")
        return 0 if success else 1
    
    def cmd_google_auth(self, args):
        """Authenticate with Google"""
        print("\n🔑 Google Authentication\n")
        
        auth_url = self.auth.get_auth_code_url()
        if not auth_url:
            print("❌ Google OAuth2 not configured")
            print("   Run: antigravity google setup --id YOUR_ID --secret YOUR_SECRET")
            return 1
        
        print("1. Open this URL in your browser:")
        print(f"\n   {auth_url}\n")
        print("2. Copy the authorization code")
        print("3. Run: antigravity google auth --code YOUR_CODE\n")
        
        if args.code:
            success = self.auth.exchange_code_for_token(args.code)
            return 0 if success else 1
        
        return 0
    
    def cmd_google_status(self, args):
        """Check auth status"""
        status = self.auth.get_auth_status()
        print(f"\n📊 Authentication Status\n")
        print(f"Status: {status['status']}")
        print(f"Message: {status['message']}")
        if 'obtained_at' in status:
            print(f"Obtained: {status['obtained_at']}")
        print()
        return 0
    
    def cmd_google_list(self, args):
        """List Drive files"""
        print("\n📄 Google Drive Files\n")
        files = self.drive.list_files()
        if not files:
            print("No files found (or not authenticated)\n")
            return 0
        
        for f in files:
            print(f"  {f.get('name', 'Unknown')} - {f.get('size', 'N/A')}")
        print()
        return 0
    
    def cmd_google_upload(self, args):
        """Upload file to Drive"""
        success = self.drive.upload_file(args.file, args.path)
        print()
        return 0 if success else 1
    
    def cmd_google_download(self, args):
        """Download from Drive"""
        success = self.drive.download_file(args.file_id, args.output)
        print()
        return 0 if success else 1
    
    def cmd_google_help(self, args):
        """Show Google help"""
        print("""\nGoogle OAuth2 Management:
  antigravity google setup --id ID --secret SECRET
  antigravity google auth [--code CODE]
  antigravity google status
  antigravity google list
  antigravity google upload FILE [--path PATH]
  antigravity google download FILE_ID --output PATH
        """)
        return 0
    
    # Drive commands
    def cmd_drive_sync(self, args):
        """Sync folder"""
        success = self.drive.sync_folder(args.folder, args.path)
        print()
        return 0 if success else 1
    
    def cmd_drive_quota(self, args):
        """Show quota"""
        print("\n📊 Google Drive Quota\n")
        quota = self.drive.list_quota()
        for key, val in quota.items():
            print(f"  {key}: {val}")
        print()
        return 0
    
    def cmd_drive_mkdir(self, args):
        """Create folder"""
        folder_id = self.drive.create_folder(args.name, args.parent)
        if folder_id:
            print(f"\n✅ Created folder: {folder_id}\n")
            return 0
        return 1
    
    def cmd_drive_help(self, args):
        """Show Drive help"""
        print("""\nGoogle Drive Operations:
  antigravity drive sync FOLDER [--path PATH]
  antigravity drive quota
  antigravity drive mkdir NAME [--parent ID]
        """)
        return 0
    
    # Info commands
    def cmd_info_device(self, args):
        """Show device info"""
        print("\n📱 Device Information\n")
        info = TermuxUtils.get_device_info()
        for key, val in info.items():
            print(f"  {key}: {val}")
        
        is_termux = TermuxUtils.is_termux()
        print(f"  running_in_termux: {is_termux}")
        print()
        return 0
    
    def cmd_info_storage(self, args):
        """Show storage paths"""
        print("\n📁 Storage Paths\n")
        paths = TermuxUtils.get_storage_paths()
        if not paths:
            print("  No storage paths found")
            print("  Run: termux-setup-storage\n")
            return 0
        
        for name, path in paths.items():
            print(f"  {name}: {path}")
        print()
        return 0


def main(args=None):
    """Entry point"""
    cli = AntiGravityCLI()
    return cli.run(args)
