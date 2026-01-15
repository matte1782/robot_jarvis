"""
JARVIS Debug Buddy Workflow
Assists with debugging, error analysis, and fix suggestions

Features:
- Stack trace parsing and analysis
- Error classification and root cause identification
- Log pattern analysis
- Suggested fixes with code snippets
- Environment comparison

Usage:
    from workflows.debug_buddy import DebugBuddy

    buddy = DebugBuddy()
    analysis = buddy.analyze_error(traceback_text)
    suggestions = buddy.suggest_fixes(analysis)
"""

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import json


@dataclass
class StackFrame:
    """A single frame in a stack trace"""
    file: str
    line: int
    function: str
    code: Optional[str] = None


@dataclass
class ErrorInfo:
    """Parsed error information"""
    error_type: str
    error_message: str
    stack_frames: List[StackFrame] = field(default_factory=list)
    root_frame: Optional[StackFrame] = None
    category: str = "unknown"  # syntax, runtime, logic, environment
    severity: str = "error"


@dataclass
class LogPattern:
    """A detected pattern in logs"""
    pattern_type: str  # "repeated_error", "slow_operation", "memory_spike", etc.
    count: int
    sample: str
    first_occurrence: Optional[str] = None
    last_occurrence: Optional[str] = None


@dataclass
class FixSuggestion:
    """A suggested fix for an error"""
    title: str
    description: str
    code_before: Optional[str] = None
    code_after: Optional[str] = None
    confidence: float = 0.0  # 0-1
    references: List[str] = field(default_factory=list)


class DebugBuddy:
    """
    Debug Buddy workflow for JARVIS.
    Provides error analysis and debugging assistance.
    """

    # Common error patterns and their fixes
    ERROR_PATTERNS = {
        # AttributeError patterns
        r"'NoneType' object has no attribute '(\w+)'": {
            "category": "runtime",
            "cause": "Trying to access attribute on None value",
            "fix_template": "Add null check before accessing attribute",
        },
        r"'(\w+)' object has no attribute '(\w+)'": {
            "category": "runtime",
            "cause": "Object doesn't have expected attribute",
            "fix_template": "Check object type or use hasattr()",
        },

        # TypeError patterns
        r"unsupported operand type\(s\) for (\+|\-|\*|\/): '(\w+)' and '(\w+)'": {
            "category": "runtime",
            "cause": "Type mismatch in operation",
            "fix_template": "Convert types before operation",
        },
        r"'(\w+)' object is not callable": {
            "category": "runtime",
            "cause": "Trying to call a non-function",
            "fix_template": "Check if you're using parentheses correctly",
        },
        r"'(\w+)' object is not subscriptable": {
            "category": "runtime",
            "cause": "Trying to index a non-indexable object",
            "fix_template": "Verify object type supports indexing",
        },

        # KeyError / IndexError
        r"KeyError: '?(\w+)'?": {
            "category": "runtime",
            "cause": "Dictionary key not found",
            "fix_template": "Use .get() with default or check key existence",
        },
        r"list index out of range": {
            "category": "runtime",
            "cause": "Index exceeds list length",
            "fix_template": "Check list length before accessing",
        },

        # ImportError / ModuleNotFoundError
        r"No module named '([\w\.]+)'": {
            "category": "environment",
            "cause": "Module not installed or not in path",
            "fix_template": "Install with pip or check PYTHONPATH",
        },
        r"cannot import name '(\w+)' from '([\w\.]+)'": {
            "category": "environment",
            "cause": "Name not exported from module",
            "fix_template": "Check spelling or module version",
        },

        # FileNotFoundError
        r"No such file or directory: '([^']+)'": {
            "category": "environment",
            "cause": "File path doesn't exist",
            "fix_template": "Verify file path and permissions",
        },

        # SyntaxError
        r"SyntaxError: invalid syntax": {
            "category": "syntax",
            "cause": "Python syntax error",
            "fix_template": "Check for missing colons, parentheses, or quotes",
        },
        r"SyntaxError: unexpected EOF": {
            "category": "syntax",
            "cause": "Incomplete code block",
            "fix_template": "Check for unclosed brackets or quotes",
        },

        # ValueError
        r"invalid literal for int\(\) with base (\d+): '([^']*)'": {
            "category": "runtime",
            "cause": "Cannot convert string to integer",
            "fix_template": "Validate input before conversion",
        },

        # PermissionError
        r"Permission denied": {
            "category": "environment",
            "cause": "Insufficient file system permissions",
            "fix_template": "Check file permissions or run with elevated privileges",
        },

        # ConnectionError
        r"Connection refused|Connection reset|Connection timed out": {
            "category": "environment",
            "cause": "Network connection failed",
            "fix_template": "Check network, server status, and firewall",
        },
    }

    def __init__(self, project_root: Optional[str] = None):
        """
        Initialize Debug Buddy.

        Args:
            project_root: Root directory of the project (for context)
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()

    def parse_traceback(self, traceback_text: str) -> ErrorInfo:
        """
        Parse a Python traceback into structured data.

        Args:
            traceback_text: The full traceback text

        Returns:
            Parsed ErrorInfo
        """
        lines = traceback_text.strip().split("\n")
        frames = []
        error_type = ""
        error_message = ""

        # Parse stack frames
        # Format: '  File "path", line N, in function'
        frame_pattern = r'\s*File "([^"]+)", line (\d+), in (\w+|<\w+>)'
        code_line = None

        for i, line in enumerate(lines):
            match = re.match(frame_pattern, line)
            if match:
                file_path, line_num, func_name = match.groups()

                # Next line might be the code
                if i + 1 < len(lines) and not lines[i + 1].startswith("  File"):
                    code_line = lines[i + 1].strip()
                else:
                    code_line = None

                frames.append(StackFrame(
                    file=file_path,
                    line=int(line_num),
                    function=func_name,
                    code=code_line
                ))

        # Parse error line (usually last line)
        error_line = lines[-1] if lines else ""
        error_match = re.match(r"(\w+Error|\w+Exception): (.+)", error_line)
        if error_match:
            error_type = error_match.group(1)
            error_message = error_match.group(2)
        else:
            # Try simpler pattern
            parts = error_line.split(":", 1)
            if len(parts) == 2:
                error_type = parts[0].strip()
                error_message = parts[1].strip()
            else:
                error_type = "UnknownError"
                error_message = error_line

        # Determine category
        category = self._categorize_error(error_type, error_message)

        return ErrorInfo(
            error_type=error_type,
            error_message=error_message,
            stack_frames=frames,
            root_frame=frames[-1] if frames else None,
            category=category,
            severity="error"
        )

    def _categorize_error(self, error_type: str, error_message: str) -> str:
        """Categorize the error type"""
        if error_type == "SyntaxError":
            return "syntax"
        elif error_type in ["ModuleNotFoundError", "ImportError", "FileNotFoundError",
                           "PermissionError", "ConnectionError"]:
            return "environment"
        elif error_type in ["AttributeError", "TypeError", "KeyError", "IndexError",
                           "ValueError", "ZeroDivisionError"]:
            return "runtime"
        else:
            return "unknown"

    def analyze_error(self, traceback_text: str) -> Dict[str, Any]:
        """
        Analyze an error and provide detailed information.

        Args:
            traceback_text: The full traceback text

        Returns:
            Analysis dictionary
        """
        error = self.parse_traceback(traceback_text)

        # Find matching pattern
        pattern_match = None
        for pattern, info in self.ERROR_PATTERNS.items():
            if re.search(pattern, error.error_message, re.IGNORECASE):
                pattern_match = (pattern, info)
                break

        analysis = {
            "error_type": error.error_type,
            "error_message": error.error_message,
            "category": error.category,
            "severity": error.severity,
            "root_cause": {
                "file": error.root_frame.file if error.root_frame else "unknown",
                "line": error.root_frame.line if error.root_frame else 0,
                "function": error.root_frame.function if error.root_frame else "unknown",
                "code": error.root_frame.code if error.root_frame else None,
            },
            "stack_depth": len(error.stack_frames),
            "frames": [
                {
                    "file": f.file,
                    "line": f.line,
                    "function": f.function,
                    "code": f.code
                }
                for f in error.stack_frames
            ]
        }

        if pattern_match:
            _, info = pattern_match
            analysis["pattern_match"] = {
                "cause": info["cause"],
                "category": info["category"],
                "fix_hint": info["fix_template"]
            }

        return analysis

    def suggest_fixes(self, analysis: Dict[str, Any]) -> List[FixSuggestion]:
        """
        Generate fix suggestions based on error analysis.

        Args:
            analysis: Output from analyze_error()

        Returns:
            List of fix suggestions
        """
        suggestions = []
        error_type = analysis["error_type"]
        error_message = analysis["error_message"]
        root_cause = analysis.get("root_cause", {})

        # Generate specific suggestions based on error type
        if error_type == "AttributeError" and "'NoneType'" in error_message:
            attr_match = re.search(r"'(\w+)'$", error_message)
            attr_name = attr_match.group(1) if attr_match else "attribute"

            suggestions.append(FixSuggestion(
                title="Add None check",
                description=f"Check if the object is None before accessing .{attr_name}",
                code_before=f"result = obj.{attr_name}",
                code_after=f"""if obj is not None:
    result = obj.{attr_name}
else:
    result = default_value  # or raise appropriate error""",
                confidence=0.9,
                references=["https://docs.python.org/3/library/stdtypes.html#truth-value-testing"]
            ))

            suggestions.append(FixSuggestion(
                title="Use getattr() with default",
                description="Use getattr() to safely access attribute with a default value",
                code_before=f"result = obj.{attr_name}",
                code_after=f"result = getattr(obj, '{attr_name}', default_value)",
                confidence=0.7
            ))

        elif error_type == "KeyError":
            key_match = re.search(r"KeyError: ['\"]?(\w+)['\"]?", str(analysis))
            key_name = key_match.group(1) if key_match else "key"

            suggestions.append(FixSuggestion(
                title="Use .get() method",
                description="Use dict.get() to safely access with a default value",
                code_before=f"value = my_dict['{key_name}']",
                code_after=f"value = my_dict.get('{key_name}', default_value)",
                confidence=0.9,
                references=["https://docs.python.org/3/library/stdtypes.html#dict.get"]
            ))

            suggestions.append(FixSuggestion(
                title="Check key existence",
                description="Check if the key exists before accessing",
                code_before=f"value = my_dict['{key_name}']",
                code_after=f"""if '{key_name}' in my_dict:
    value = my_dict['{key_name}']
else:
    value = default_value""",
                confidence=0.8
            ))

        elif error_type == "IndexError":
            suggestions.append(FixSuggestion(
                title="Check list length",
                description="Verify the list has enough elements before accessing",
                code_before="item = my_list[index]",
                code_after="""if index < len(my_list):
    item = my_list[index]
else:
    item = default_value  # or handle appropriately""",
                confidence=0.9
            ))

        elif error_type in ["ModuleNotFoundError", "ImportError"]:
            module_match = re.search(r"No module named '([\w\.]+)'", error_message)
            module_name = module_match.group(1) if module_match else "module"

            suggestions.append(FixSuggestion(
                title="Install missing module",
                description=f"Install the missing module with pip",
                code_before=f"# Module '{module_name}' not found",
                code_after=f"# Run: pip install {module_name}",
                confidence=0.8,
                references=[f"https://pypi.org/project/{module_name}/"]
            ))

        elif error_type == "FileNotFoundError":
            suggestions.append(FixSuggestion(
                title="Check file exists",
                description="Verify the file exists before opening",
                code_before='with open(path) as f:',
                code_after='''from pathlib import Path

if Path(path).exists():
    with open(path) as f:
        # process file
else:
    # handle missing file''',
                confidence=0.9
            ))

        # Add general suggestions
        if not suggestions:
            suggestions.append(FixSuggestion(
                title="Add debugging",
                description="Add print statements or logging to investigate",
                code_after="""import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add before the error:
logger.debug(f"Variable value: {variable}")""",
                confidence=0.5
            ))

        return suggestions

    def format_analysis(self, analysis: Dict[str, Any],
                       suggestions: List[FixSuggestion]) -> str:
        """
        Format analysis and suggestions as markdown.

        Args:
            analysis: Error analysis
            suggestions: List of fix suggestions

        Returns:
            Markdown-formatted report
        """
        report = f"""## Error Analysis

### Error Details
- **Type**: `{analysis['error_type']}`
- **Message**: {analysis['error_message']}
- **Category**: {analysis['category'].title()}

### Location
- **File**: `{analysis['root_cause']['file']}`
- **Line**: {analysis['root_cause']['line']}
- **Function**: `{analysis['root_cause']['function']}`

"""

        if analysis['root_cause'].get('code'):
            report += f"""### Problematic Code
```python
{analysis['root_cause']['code']}
```

"""

        if 'pattern_match' in analysis:
            pm = analysis['pattern_match']
            report += f"""### Root Cause Analysis
**Cause**: {pm['cause']}

**Quick Fix Hint**: {pm['fix_hint']}

"""

        report += f"""### Stack Trace Summary
{analysis['stack_depth']} frames in call stack

"""

        # Add frames (limit to first and last few)
        frames = analysis['frames']
        if len(frames) > 4:
            for f in frames[:2]:
                report += f"- `{f['file']}:{f['line']}` in `{f['function']}`\n"
            report += f"- ... ({len(frames) - 4} more frames)\n"
            for f in frames[-2:]:
                report += f"- `{f['file']}:{f['line']}` in `{f['function']}`\n"
        else:
            for f in frames:
                report += f"- `{f['file']}:{f['line']}` in `{f['function']}`\n"

        report += "\n---\n\n## Suggested Fixes\n\n"

        for i, fix in enumerate(suggestions, 1):
            confidence_emoji = "" if fix.confidence >= 0.8 else "" if fix.confidence >= 0.5 else ""
            report += f"### {i}. {fix.title} {confidence_emoji}\n\n"
            report += f"{fix.description}\n\n"

            if fix.code_before:
                report += "**Before:**\n```python\n"
                report += fix.code_before
                report += "\n```\n\n"

            if fix.code_after:
                report += "**After:**\n```python\n"
                report += fix.code_after
                report += "\n```\n\n"

            if fix.references:
                report += "**References:**\n"
                for ref in fix.references:
                    report += f"- {ref}\n"
                report += "\n"

        return report

    def analyze_logs(self, log_text: str) -> List[LogPattern]:
        """
        Analyze log file for patterns and issues.

        Args:
            log_text: Log file contents

        Returns:
            List of detected patterns
        """
        patterns = []
        lines = log_text.split("\n")

        # Count error occurrences
        error_counts: Dict[str, List[str]] = {}
        for line in lines:
            if re.search(r'\b(error|exception|fail|critical)\b', line, re.IGNORECASE):
                # Normalize the error message
                key = re.sub(r'\d+', 'N', line)[:100]  # Replace numbers, limit length
                if key not in error_counts:
                    error_counts[key] = []
                error_counts[key].append(line)

        # Report repeated errors
        for key, occurrences in error_counts.items():
            if len(occurrences) >= 3:
                patterns.append(LogPattern(
                    pattern_type="repeated_error",
                    count=len(occurrences),
                    sample=occurrences[0],
                    first_occurrence=occurrences[0][:50],
                    last_occurrence=occurrences[-1][:50]
                ))

        # Detect slow operations
        slow_pattern = r'took (\d+(?:\.\d+)?)\s*(ms|s|seconds?)'
        for line in lines:
            match = re.search(slow_pattern, line, re.IGNORECASE)
            if match:
                duration = float(match.group(1))
                unit = match.group(2).lower()
                if unit in ['s', 'second', 'seconds']:
                    duration *= 1000  # Convert to ms
                if duration > 1000:  # More than 1 second
                    patterns.append(LogPattern(
                        pattern_type="slow_operation",
                        count=1,
                        sample=line
                    ))

        return patterns


# CLI interface
def main():
    """CLI for Debug Buddy"""
    import sys

    buddy = DebugBuddy()

    if len(sys.argv) < 2:
        print("Usage: python debug_buddy.py [command]")
        print("Commands:")
        print("  analyze   - Analyze error from stdin")
        print("  logs      - Analyze logs from stdin")
        print("")
        print("Example:")
        print("  cat traceback.txt | python debug_buddy.py analyze")
        return

    command = sys.argv[1]

    if command == "analyze":
        # Read traceback from stdin
        traceback_text = sys.stdin.read()
        analysis = buddy.analyze_error(traceback_text)
        suggestions = buddy.suggest_fixes(analysis)
        print(buddy.format_analysis(analysis, suggestions))

    elif command == "logs":
        log_text = sys.stdin.read()
        patterns = buddy.analyze_logs(log_text)

        print("## Log Analysis\n")
        if not patterns:
            print("No significant patterns detected.")
        else:
            for p in patterns:
                print(f"### {p.pattern_type.replace('_', ' ').title()}")
                print(f"- Count: {p.count}")
                print(f"- Sample: `{p.sample[:100]}`")
                print()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
