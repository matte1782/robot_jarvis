"""
JARVIS PR Helper Workflow
Assists with pull request creation, review, and improvements

Features:
- Generate PR descriptions from commits
- Code review assistance with actionable feedback
- Suggest improvements for code quality
- Pre-commit checks

Usage:
    from workflows.pr_helper import PRHelper

    helper = PRHelper(repo_path="/path/to/repo")
    description = await helper.generate_pr_description()
    review = await helper.review_changes()
"""

import subprocess
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class CommitInfo:
    """Information about a git commit"""
    hash: str
    short_hash: str
    author: str
    date: str
    message: str
    files_changed: int
    insertions: int
    deletions: int


@dataclass
class ReviewFinding:
    """A finding from code review"""
    file: str
    line: Optional[int]
    severity: str  # "error", "warning", "suggestion"
    category: str  # "security", "performance", "style", "bug", "test"
    message: str
    suggestion: Optional[str]


class PRHelper:
    """
    PR Helper workflow for JARVIS.
    Provides tools for PR creation, review, and improvement.
    """

    def __init__(self, repo_path: Optional[str] = None):
        """
        Initialize PR Helper.

        Args:
            repo_path: Path to git repository (default: current directory)
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()

        # Verify it's a git repo
        if not (self.repo_path / ".git").exists():
            raise ValueError(f"Not a git repository: {self.repo_path}")

    def _run_git(self, args: List[str], check: bool = True) -> str:
        """
        Run a git command safely.

        Args:
            args: Git command arguments
            check: Whether to check return code

        Returns:
            Command output
        """
        result = subprocess.run(
            ["git"] + args,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            shell=False,  # SECURITY: Never use shell=True
            timeout=30
        )

        if check and result.returncode != 0:
            raise RuntimeError(f"Git command failed: {result.stderr}")

        return result.stdout.strip()

    def get_current_branch(self) -> str:
        """Get the current branch name"""
        return self._run_git(["rev-parse", "--abbrev-ref", "HEAD"])

    def get_base_branch(self) -> str:
        """
        Detect the base branch (main/master).

        Returns:
            Name of the base branch
        """
        # Try common base branch names
        for branch in ["main", "master", "develop"]:
            try:
                self._run_git(["rev-parse", "--verify", branch])
                return branch
            except RuntimeError:
                continue

        # Fallback to origin/HEAD
        try:
            ref = self._run_git(["symbolic-ref", "refs/remotes/origin/HEAD"])
            return ref.split("/")[-1]
        except RuntimeError:
            return "main"  # Default assumption

    def get_commits_since_base(self, base_branch: Optional[str] = None) -> List[CommitInfo]:
        """
        Get commits since the base branch.

        Args:
            base_branch: Base branch to compare against

        Returns:
            List of commit information
        """
        base = base_branch or self.get_base_branch()

        # Get commit log
        log_format = "%H|%h|%an|%ad|%s"
        log_output = self._run_git([
            "log", f"{base}..HEAD",
            f"--format={log_format}",
            "--date=short"
        ])

        if not log_output:
            return []

        commits = []
        for line in log_output.split("\n"):
            if not line:
                continue

            parts = line.split("|")
            if len(parts) < 5:
                continue

            full_hash, short_hash, author, date, message = parts[:5]

            # Get stats for this commit
            stat_output = self._run_git([
                "show", short_hash,
                "--stat", "--format="
            ])

            files, insertions, deletions = 0, 0, 0
            stat_match = re.search(
                r"(\d+) files? changed(?:, (\d+) insertions?\(\+\))?(?:, (\d+) deletions?\(-\))?",
                stat_output
            )
            if stat_match:
                files = int(stat_match.group(1) or 0)
                insertions = int(stat_match.group(2) or 0)
                deletions = int(stat_match.group(3) or 0)

            commits.append(CommitInfo(
                hash=full_hash,
                short_hash=short_hash,
                author=author,
                date=date,
                message=message,
                files_changed=files,
                insertions=insertions,
                deletions=deletions
            ))

        return commits

    def get_diff(self, base_branch: Optional[str] = None, staged_only: bool = False) -> str:
        """
        Get the diff for review.

        Args:
            base_branch: Base branch to compare against
            staged_only: Only show staged changes

        Returns:
            Diff output
        """
        if staged_only:
            return self._run_git(["diff", "--staged"])
        else:
            base = base_branch or self.get_base_branch()
            return self._run_git(["diff", f"{base}...HEAD"])

    def get_changed_files(self, base_branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get list of changed files with stats.

        Returns:
            List of file change info
        """
        base = base_branch or self.get_base_branch()
        output = self._run_git(["diff", f"{base}...HEAD", "--stat", "--name-status"])

        files = []
        for line in output.split("\n"):
            if not line or "|" in line:  # Skip stat summary lines
                continue

            parts = line.split("\t")
            if len(parts) >= 2:
                status, filepath = parts[0], parts[-1]
                status_map = {
                    "A": "added",
                    "M": "modified",
                    "D": "deleted",
                    "R": "renamed"
                }
                files.append({
                    "path": filepath,
                    "status": status_map.get(status[0], "unknown")
                })

        return files

    def generate_pr_description(self, base_branch: Optional[str] = None) -> str:
        """
        Generate a PR description based on commits and changes.

        Args:
            base_branch: Base branch to compare against

        Returns:
            Markdown-formatted PR description
        """
        commits = self.get_commits_since_base(base_branch)
        changed_files = self.get_changed_files(base_branch)
        current_branch = self.get_current_branch()

        if not commits:
            return "No commits found for this PR."

        # Analyze commits to categorize changes
        total_insertions = sum(c.insertions for c in commits)
        total_deletions = sum(c.deletions for c in commits)

        # Determine PR type from commit messages
        pr_type = "Feature"
        commit_messages_lower = " ".join(c.message.lower() for c in commits)
        if "fix" in commit_messages_lower or "bug" in commit_messages_lower:
            pr_type = "Bug Fix"
        elif "refactor" in commit_messages_lower:
            pr_type = "Refactor"
        elif "test" in commit_messages_lower:
            pr_type = "Tests"
        elif "doc" in commit_messages_lower:
            pr_type = "Documentation"

        # Build description
        description = f"""## Summary
<!-- Brief description of what this PR does -->
{pr_type}: {commits[0].message}

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Changes Made
<!-- List the main changes -->
"""

        # Add commit summary
        for commit in commits[:10]:  # Limit to 10 commits
            description += f"- {commit.message} ({commit.short_hash})\n"

        if len(commits) > 10:
            description += f"- ... and {len(commits) - 10} more commits\n"

        description += f"""
## Files Changed
{len(changed_files)} files changed (+{total_insertions}, -{total_deletions})

| File | Status |
|------|--------|
"""

        for f in changed_files[:20]:  # Limit to 20 files
            description += f"| `{f['path']}` | {f['status']} |\n"

        if len(changed_files) > 20:
            description += f"| ... | +{len(changed_files) - 20} more |\n"

        description += """
## Testing Done
<!-- Describe the testing you've done -->
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
<!-- Add screenshots for UI changes -->

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
"""

        return description

    def analyze_for_review(self, base_branch: Optional[str] = None) -> List[ReviewFinding]:
        """
        Analyze changes for potential issues.

        This is a basic static analysis - for full review,
        integrate with LLM analysis.

        Returns:
            List of review findings
        """
        findings = []
        diff = self.get_diff(base_branch)

        # Basic pattern checks for security and code quality issues
        # NOTE: These patterns are used for DETECTION, not execution
        patterns = [
            # Security patterns to detect
            (r'password\s*=\s*["\'][^"\']+["\']', "security", "error",
             "Possible hardcoded password", "Use environment variables or secrets manager"),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', "security", "error",
             "Possible hardcoded API key", "Use environment variables"),

            # Performance
            (r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(', "performance", "suggestion",
             "Use enumerate() instead of range(len())", "for i, item in enumerate(items):"),

            # Code quality
            (r'except\s*:', "bug", "warning",
             "Bare except clause catches all exceptions", "Specify exception type: except Exception:"),
            (r'# TODO', "style", "suggestion",
             "TODO comment found", "Consider creating an issue to track this"),
            (r'print\s*\(', "style", "suggestion",
             "Print statement found", "Consider using logging instead"),
        ]

        # Parse diff to get file context
        current_file = None
        current_line = 0

        for line in diff.split("\n"):
            # Track file changes
            if line.startswith("+++ b/"):
                current_file = line[6:]
                current_line = 0
                continue

            # Track line numbers
            if line.startswith("@@"):
                match = re.search(r'\+(\d+)', line)
                if match:
                    current_line = int(match.group(1))
                continue

            # Only check added lines
            if line.startswith("+") and not line.startswith("+++"):
                content = line[1:]
                current_line += 1

                for pattern, category, severity, message, suggestion in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        findings.append(ReviewFinding(
                            file=current_file or "unknown",
                            line=current_line,
                            severity=severity,
                            category=category,
                            message=message,
                            suggestion=suggestion
                        ))

        return findings

    def format_review_findings(self, findings: List[ReviewFinding]) -> str:
        """
        Format review findings as markdown.

        Args:
            findings: List of review findings

        Returns:
            Markdown-formatted review
        """
        if not findings:
            return "## Code Review\n\nNo issues found. LGTM!"

        # Group by severity
        errors = [f for f in findings if f.severity == "error"]
        warnings = [f for f in findings if f.severity == "warning"]
        suggestions = [f for f in findings if f.severity == "suggestion"]

        review = "## Code Review\n\n"

        if errors:
            review += "### Errors (Must Fix)\n"
            for f in errors:
                review += f"- **{f.file}:{f.line}** [{f.category}] {f.message}\n"
                if f.suggestion:
                    review += f"  - Suggestion: {f.suggestion}\n"
            review += "\n"

        if warnings:
            review += "### Warnings (Should Fix)\n"
            for f in warnings:
                review += f"- **{f.file}:{f.line}** [{f.category}] {f.message}\n"
                if f.suggestion:
                    review += f"  - Suggestion: {f.suggestion}\n"
            review += "\n"

        if suggestions:
            review += "### Suggestions (Nice to Have)\n"
            for f in suggestions:
                review += f"- **{f.file}:{f.line}** [{f.category}] {f.message}\n"
                if f.suggestion:
                    review += f"  - Suggestion: {f.suggestion}\n"
            review += "\n"

        review += f"\n**Summary**: {len(errors)} errors, {len(warnings)} warnings, {len(suggestions)} suggestions\n"

        return review

    def suggest_commit_message(self) -> str:
        """
        Suggest a commit message based on staged changes.

        Returns:
            Suggested commit message
        """
        # Get staged diff
        diff = self._run_git(["diff", "--staged", "--stat"])

        if not diff:
            return "No staged changes"

        # Get staged files
        files = self._run_git(["diff", "--staged", "--name-only"])
        file_list = files.split("\n") if files else []

        # Determine type based on files
        msg_type = "chore"
        if any("test" in f.lower() for f in file_list):
            msg_type = "test"
        elif any(f.endswith(".md") for f in file_list):
            msg_type = "docs"
        elif any("fix" in f.lower() for f in file_list):
            msg_type = "fix"
        else:
            msg_type = "feat"

        # Determine scope from common path
        if file_list:
            parts = file_list[0].split("/")
            scope = parts[0] if len(parts) > 1 else ""
        else:
            scope = ""

        # Build message template
        scope_part = f"({scope})" if scope else ""
        message = f"{msg_type}{scope_part}: describe your changes here"

        return message


# CLI interface
def main():
    """CLI for PR Helper"""
    import sys

    helper = PRHelper()

    if len(sys.argv) < 2:
        print("Usage: python pr_helper.py [command]")
        print("Commands:")
        print("  describe    - Generate PR description")
        print("  review      - Review changes")
        print("  suggest-msg - Suggest commit message")
        return

    command = sys.argv[1]

    if command == "describe":
        print(helper.generate_pr_description())
    elif command == "review":
        findings = helper.analyze_for_review()
        print(helper.format_review_findings(findings))
    elif command == "suggest-msg":
        print(helper.suggest_commit_message())
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
