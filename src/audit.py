"""
JARVIS Security Audit Logger
Logs security-relevant events for review and compliance.
"""
import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
from logging.handlers import RotatingFileHandler


class AuditLogger:
    """
    Security audit logger with file-based persistence.

    Logs:
    - Authentication attempts
    - Command executions
    - File operations
    - Rate limit events
    - Security violations
    """

    # Event types
    AUTH_SUCCESS = "AUTH_SUCCESS"
    AUTH_FAILURE = "AUTH_FAILURE"
    COMMAND_EXEC = "COMMAND_EXEC"
    COMMAND_BLOCKED = "COMMAND_BLOCKED"
    FILE_READ = "FILE_READ"
    FILE_WRITE = "FILE_WRITE"
    FILE_BLOCKED = "FILE_BLOCKED"
    RATE_LIMIT = "RATE_LIMIT"
    SECURITY_VIOLATION = "SECURITY_VIOLATION"

    def __init__(
        self,
        log_dir: Optional[str] = None,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5
    ):
        """
        Initialize audit logger.

        Args:
            log_dir: Directory for audit logs (default: ./logs)
            max_bytes: Max size per log file before rotation
            backup_count: Number of backup files to keep
        """
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')

        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Set up rotating file handler
        self.logger = logging.getLogger('jarvis.audit')
        self.logger.setLevel(logging.INFO)

        # Avoid duplicate handlers
        if not self.logger.handlers:
            handler = RotatingFileHandler(
                self.log_dir / 'audit.log',
                maxBytes=max_bytes,
                backupCount=backup_count
            )
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log(
        self,
        event_type: str,
        details: Dict[str, Any],
        severity: str = "INFO"
    ) -> None:
        """
        Log an audit event.

        Args:
            event_type: Type of event (use class constants)
            details: Event details dictionary
            severity: Log level (INFO, WARNING, ERROR)
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "details": details
        }

        message = json.dumps(record)

        if severity == "ERROR":
            self.logger.error(message)
        elif severity == "WARNING":
            self.logger.warning(message)
        else:
            self.logger.info(message)

    def log_auth(self, success: bool, client_id: str, reason: str = "") -> None:
        """Log authentication attempt"""
        event = self.AUTH_SUCCESS if success else self.AUTH_FAILURE
        self.log(
            event,
            {"client": client_id, "reason": reason},
            severity="INFO" if success else "WARNING"
        )

    def log_command(
        self,
        command: str,
        allowed: bool,
        reason: str = ""
    ) -> None:
        """Log command execution attempt"""
        event = self.COMMAND_EXEC if allowed else self.COMMAND_BLOCKED
        self.log(
            event,
            {"command": command, "reason": reason},
            severity="INFO" if allowed else "WARNING"
        )

    def log_file_access(
        self,
        path: str,
        operation: str,
        allowed: bool,
        reason: str = ""
    ) -> None:
        """Log file access attempt"""
        if operation == "read":
            event = self.FILE_READ if allowed else self.FILE_BLOCKED
        else:
            event = self.FILE_WRITE if allowed else self.FILE_BLOCKED

        self.log(
            event,
            {"path": path, "operation": operation, "reason": reason},
            severity="INFO" if allowed else "WARNING"
        )

    def log_rate_limit(self, client_id: str, endpoint: str) -> None:
        """Log rate limit event"""
        self.log(
            self.RATE_LIMIT,
            {"client": client_id, "endpoint": endpoint},
            severity="WARNING"
        )

    def log_security_violation(
        self,
        violation_type: str,
        details: Dict[str, Any]
    ) -> None:
        """Log security violation"""
        self.log(
            self.SECURITY_VIOLATION,
            {"type": violation_type, **details},
            severity="ERROR"
        )


# Singleton instance
_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> AuditLogger:
    """Get or create default audit logger"""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger
