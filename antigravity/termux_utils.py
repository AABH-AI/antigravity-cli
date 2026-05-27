"""Termux-specific utilities"""

import subprocess
import os
from pathlib import Path
from typing import Optional, Dict

class TermuxUtils:
    """Utilities for Termux environment"""
    
    @staticmethod
    def is_termux() -> bool:
        """Check if running in Termux"""
        return os.path.exists("/data/data/com.termux")
    
    @staticmethod
    def get_termux_home() -> Path:
        """Get Termux home directory"""
        if TermuxUtils.is_termux():
            return Path.home()
        return Path.home()
    
    @staticmethod
    def get_storage_paths() -> Dict[str, Path]:
        """Get important storage paths in Termux"""
        home = TermuxUtils.get_termux_home()
        
        paths = {
            "home": home,
            "storage": home / "storage",
            "downloads": home / "storage" / "downloads",
            "documents": home / "storage" / "documents",
            "pictures": home / "storage" / "pictures",
        }
        
        # Filter existing paths
        return {k: v for k, v in paths.items() if v.exists()}
    
    @staticmethod
    def request_storage_permission() -> bool:
        """Request storage permission in Termux"""
        try:
            result = subprocess.run(
                ["termux-setup-storage"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            print("⚠️  Run 'termux-setup-storage' in Termux to grant storage access")
            return False
    
    @staticmethod
    def show_notification(title: str, message: str) -> bool:
        """Show Android notification from Termux"""
        try:
            subprocess.run(
                ["termux-notification", "--title", title, "--content", message],
                capture_output=True,
                timeout=5
            )
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_device_info() -> Dict:
        """Get device information"""
        info = {
            "platform": "Termux",
            "python_version": __import__("sys").version,
        }
        
        try:
            import platform
            info["system"] = platform.system()
            info["machine"] = platform.machine()
        except:
            pass
        
        return info
