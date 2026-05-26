"""System information and health checks"""
import os
import subprocess
try:
    import psutil
except ImportError:
    psutil = None
from pathlib import Path
from typing import Dict, Any
from ..core import AntiGravityError, Logger

class SystemInfo:
    """Get system information and health status"""
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def get_storage(self) -> Dict[str, Any]:
        try:
            stat = os.statvfs("/")
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bavail * stat.f_frsize
            used = total - free
            percent = (used / total) * 100 if total > 0 else 0
            return {"total_gb": round(total / (1024**3), 2), "free_gb": round(free / (1024**3), 2), "used_gb": round(used / (1024**3), 2), "percent_used": round(percent, 2)}
        except Exception as e:
            raise AntiGravityError(f"Failed to get storage: {e}", "", "STORAGE_ERROR")
    
    def get_memory(self) -> Dict[str, Any]:
        if psutil is None:
            return {"status": "unavailable"}
        try:
            mem = psutil.virtual_memory()
            return {"total_mb": round(mem.total / (1024**2), 2), "available_mb": round(mem.available / (1024**2), 2), "used_mb": round(mem.used / (1024**2), 2), "percent": round(mem.percent, 2)}
        except Exception:
            return {"status": "unavailable"}
    
    def get_health(self) -> Dict[str, Any]:
        return {"storage": self.get_storage(), "memory": self.get_memory(), "warnings": []}
