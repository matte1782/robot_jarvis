"""
Jarvis Authentication Module
Simple API key authentication for local use

SECURITY FEATURES:
- API keys are hashed with SHA-256 (never stored in plaintext)
- Key file has restricted permissions (owner-only)
- Constant-time comparison to prevent timing attacks
- Keys can be rotated without losing history

Usage:
    from auth import JarvisAuth

    auth = JarvisAuth()
    if auth.verify(api_key):
        # Proceed with request
    else:
        # Reject request

First run will generate and display a new API key.
"""
import secrets
import hashlib
import hmac
import json
import stat
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

# Default auth file location
DEFAULT_AUTH_DIR = Path.home() / ".jarvis"
DEFAULT_AUTH_FILE = DEFAULT_AUTH_DIR / "auth.json"

# API key settings
API_KEY_LENGTH = 32  # 256 bits of entropy
API_KEY_PREFIX = "jrv_"  # Prefix for easy identification

# Logging
logger = logging.getLogger("jarvis.auth")


# =============================================================================
# AUTHENTICATION CLASS
# =============================================================================

class JarvisAuth:
    """
    Simple API key authentication for Jarvis.

    On first initialization, generates a new API key and displays it once.
    The key is stored as a SHA-256 hash - the original key cannot be recovered.
    """

    def __init__(self, auth_file: Optional[Path] = None):
        """
        Initialize authentication.

        Args:
            auth_file: Path to auth file (default: ~/.jarvis/auth.json)
        """
        self.auth_file = auth_file or DEFAULT_AUTH_FILE
        self.data = {}
        self._load_or_create()

    def _load_or_create(self):
        """Load existing auth data or create new"""
        # Ensure directory exists with secure permissions
        self.auth_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.auth_file.parent.chmod(stat.S_IRWXU)  # 700 - owner only
        except OSError:
            pass  # Windows may not support this

        if self.auth_file.exists():
            self._load()
        else:
            self._create_new()

    def _load(self):
        """Load auth data from file"""
        try:
            self.data = json.loads(self.auth_file.read_text())
            logger.info("Loaded authentication data")
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load auth file: {e}")
            # Don't overwrite - might be a permission issue
            raise RuntimeError(f"Cannot load auth file: {e}")

    def _save(self):
        """Save auth data to file"""
        try:
            self.auth_file.write_text(json.dumps(self.data, indent=2))
            # Set restrictive permissions
            try:
                self.auth_file.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 600 - owner only
            except OSError:
                pass  # Windows may not support this
            logger.info("Saved authentication data")
        except IOError as e:
            logger.error(f"Failed to save auth file: {e}")
            raise

    def _create_new(self):
        """Create new authentication with fresh API key"""
        # Generate secure random key
        raw_key = secrets.token_urlsafe(API_KEY_LENGTH)
        api_key = f"{API_KEY_PREFIX}{raw_key}"

        # Hash the key
        key_hash = self._hash_key(api_key)

        # Store data
        self.data = {
            "version": 1,
            "api_key_hash": key_hash,
            "created": datetime.now().isoformat(),
            "key_rotations": []
        }

        self._save()

        # Display key to user (ONLY TIME IT'S SHOWN)
        print("\n" + "=" * 60)
        print("JARVIS AUTHENTICATION SETUP")
        print("=" * 60)
        print("\nA new API key has been generated.")
        print("\n*** SAVE THIS KEY - IT WILL NOT BE SHOWN AGAIN ***\n")
        print(f"  API Key: {api_key}")
        print("\nStore this key securely (password manager recommended).")
        print(f"\nAuth file: {self.auth_file}")
        print("=" * 60 + "\n")

        logger.info("Created new API key")

    def _hash_key(self, api_key: str) -> str:
        """
        Hash an API key using SHA-256.

        Args:
            api_key: The plaintext API key

        Returns:
            Hex-encoded hash
        """
        return hashlib.sha256(api_key.encode('utf-8')).hexdigest()

    def verify(self, api_key: str) -> bool:
        """
        Verify an API key.

        Uses constant-time comparison to prevent timing attacks.

        Args:
            api_key: The API key to verify

        Returns:
            True if valid, False otherwise
        """
        if not api_key:
            return False

        stored_hash = self.data.get("api_key_hash", "")
        provided_hash = self._hash_key(api_key)

        # Constant-time comparison
        return hmac.compare_digest(stored_hash, provided_hash)

    def rotate_key(self) -> str:
        """
        Rotate the API key.

        Creates a new key and archives the old hash.

        Returns:
            The new API key (displayed once, then forgotten)
        """
        # Archive old key
        old_hash = self.data.get("api_key_hash")
        if old_hash:
            rotations = self.data.get("key_rotations", [])
            rotations.append({
                "hash": old_hash,
                "rotated_at": datetime.now().isoformat()
            })
            self.data["key_rotations"] = rotations[-10:]  # Keep last 10

        # Generate new key
        raw_key = secrets.token_urlsafe(API_KEY_LENGTH)
        api_key = f"{API_KEY_PREFIX}{raw_key}"
        key_hash = self._hash_key(api_key)

        # Update data
        self.data["api_key_hash"] = key_hash
        self.data["last_rotation"] = datetime.now().isoformat()

        self._save()

        logger.info("API key rotated")
        return api_key

    def get_info(self) -> dict:
        """
        Get authentication info (without sensitive data).

        Returns:
            Dict with auth metadata
        """
        return {
            "auth_file": str(self.auth_file),
            "created": self.data.get("created"),
            "last_rotation": self.data.get("last_rotation"),
            "rotation_count": len(self.data.get("key_rotations", []))
        }


# =============================================================================
# MIDDLEWARE HELPER
# =============================================================================

def require_auth(auth: JarvisAuth, api_key: str) -> bool:
    """
    Helper function for middleware authentication.

    Args:
        auth: JarvisAuth instance
        api_key: API key from request header

    Returns:
        True if authenticated, False otherwise
    """
    if not api_key:
        logger.warning("Authentication failed: No API key provided")
        return False

    if not auth.verify(api_key):
        logger.warning("Authentication failed: Invalid API key")
        return False

    return True


# =============================================================================
# CLI
# =============================================================================

def main():
    """CLI for managing authentication"""
    import sys

    auth = JarvisAuth()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "rotate":
            print("\nRotating API key...")
            new_key = auth.rotate_key()
            print("\n*** NEW API KEY (save this!) ***")
            print(f"  {new_key}")
            print()

        elif command == "info":
            info = auth.get_info()
            print("\nAuthentication Info:")
            for key, value in info.items():
                print(f"  {key}: {value}")
            print()

        elif command == "verify":
            if len(sys.argv) > 2:
                test_key = sys.argv[2]
                if auth.verify(test_key):
                    print("Valid API key")
                else:
                    print("Invalid API key")
            else:
                print("Usage: auth.py verify <api_key>")

        else:
            print("Usage: auth.py [rotate|info|verify <key>]")
    else:
        # Just show info
        info = auth.get_info()
        print("\nJarvis Authentication")
        print(f"  File: {info['auth_file']}")
        print(f"  Created: {info['created']}")
        print(f"  Rotations: {info['rotation_count']}")
        print("\nCommands:")
        print("  python auth.py rotate  - Generate new API key")
        print("  python auth.py info    - Show auth info")
        print("  python auth.py verify <key> - Test a key")


if __name__ == "__main__":
    main()
