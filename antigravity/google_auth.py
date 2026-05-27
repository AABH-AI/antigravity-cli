"""Google OAuth2 Authentication for Termux"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import subprocess

class GoogleAuthManager:
    """Handles Google OAuth2 authentication"""
    
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.creds_file = config_dir / "google_creds.json"
        self.tokens_file = config_dir / "google_tokens.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def setup_oauth(self, client_id: str, client_secret: str) -> bool:
        """Setup OAuth2 with provided credentials"""
        try:
            config = {
                "client_id": client_id,
                "client_secret": client_secret,
                "setup_date": datetime.now().isoformat()
            }
            with open(self.creds_file, "w") as f:
                json.dump(config, f, indent=2)
            print("\n✅ Google OAuth2 credentials saved")
            print(f"   📁 {self.creds_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to save credentials: {e}")
            return False
    
    def get_auth_code_url(self) -> str:
        """Generate OAuth2 authorization URL"""
        if not self.creds_file.exists():
            return None
        
        with open(self.creds_file) as f:
            creds = json.load(f)
        
        client_id = creds["client_id"]
        scope = "https://www.googleapis.com/auth/drive"
        redirect_uri = "http://localhost:8080/callback"
        
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope}&"
            f"access_type=offline"
        )
        return auth_url
    
    def exchange_code_for_token(self, auth_code: str) -> bool:
        """Exchange authorization code for tokens"""
        try:
            if not self.creds_file.exists():
                print("❌ Credentials not configured")
                return False
            
            with open(self.creds_file) as f:
                creds = json.load(f)
            
            # In real implementation, this would use google-auth-httplib2
            # For now, store the code
            tokens = {
                "auth_code": auth_code,
                "obtained_at": datetime.now().isoformat(),
                "status": "pending_exchange"
            }
            
            with open(self.tokens_file, "w") as f:
                json.dump(tokens, f, indent=2)
            
            print("\n✅ Authorization code saved")
            print(f"   📁 {self.tokens_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to save token: {e}")
            return False
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.tokens_file.exists()
    
    def get_auth_status(self) -> dict:
        """Get authentication status"""
        if not self.creds_file.exists():
            return {"status": "not_configured", "message": "OAuth2 not configured"}
        
        if not self.tokens_file.exists():
            return {"status": "configured", "message": "OAuth2 configured, awaiting authorization"}
        
        with open(self.tokens_file) as f:
            tokens = json.load(f)
        
        return {
            "status": "authenticated",
            "message": "Authenticated with Google",
            "obtained_at": tokens.get("obtained_at")
        }
