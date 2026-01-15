"""
JARVIS Conversation Memory
Maintains conversation history for context-aware responses.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
import json
import os


@dataclass
class Message:
    """Single conversation message"""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }


class ConversationMemory:
    """
    Manages conversation history with configurable limits.

    Features:
    - Rolling window of recent messages
    - Optional persistence to file
    - Token-aware truncation (placeholder)
    """

    def __init__(
        self,
        max_messages: int = 20,
        persist_path: Optional[str] = None
    ):
        self.max_messages = max_messages
        self.persist_path = persist_path
        self.messages: List[Message] = []

        # Load existing history if persistence enabled
        if persist_path and os.path.exists(persist_path):
            self._load()

    def add(self, role: str, content: str) -> None:
        """Add a message to history"""
        msg = Message(role=role, content=content)
        self.messages.append(msg)

        # Trim if over limit
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

        # Persist if enabled
        if self.persist_path:
            self._save()

    def get_history(self) -> List[Dict]:
        """Get conversation history for LLM context"""
        return [msg.to_dict() for msg in self.messages]

    def get_context_string(self) -> str:
        """Get history as formatted string"""
        lines = []
        for msg in self.messages:
            prefix = "User" if msg.role == "user" else "JARVIS"
            lines.append(f"{prefix}: {msg.content}")
        return "\n".join(lines)

    def clear(self) -> None:
        """Clear all history"""
        self.messages = []
        if self.persist_path and os.path.exists(self.persist_path):
            os.remove(self.persist_path)

    def _save(self) -> None:
        """Save history to file"""
        if not self.persist_path:
            return
        data = [msg.to_dict() for msg in self.messages]
        with open(self.persist_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def _load(self) -> None:
        """Load history from file"""
        if not self.persist_path or not os.path.exists(self.persist_path):
            return
        try:
            with open(self.persist_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.messages = [
                Message(
                    role=m["role"],
                    content=m["content"],
                    timestamp=datetime.fromisoformat(m["timestamp"])
                )
                for m in data
            ]
        except (json.JSONDecodeError, KeyError):
            self.messages = []


# Singleton instance for easy access
_default_memory: Optional[ConversationMemory] = None


def get_memory() -> ConversationMemory:
    """Get or create default memory instance"""
    global _default_memory
    if _default_memory is None:
        _default_memory = ConversationMemory()
    return _default_memory
