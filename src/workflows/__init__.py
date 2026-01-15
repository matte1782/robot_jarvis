"""
JARVIS Workflow Implementations
Practical daily workflows for programmers

Workflows:
- PR Helper: Generate PR descriptions, code review, improvements
- Debug Buddy: Error analysis, log parsing, fix suggestions
- Study Summarizer: Document summaries, flashcards, explanations
- Workload Manager: Task tracking, daily planning, meeting prep
"""

from .pr_helper import PRHelper
from .debug_buddy import DebugBuddy
from .study_summarizer import StudySummarizer
from .workload_manager import WorkloadManager

__all__ = [
    "PRHelper",
    "DebugBuddy",
    "StudySummarizer",
    "WorkloadManager",
]
