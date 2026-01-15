"""
JARVIS Study Summarizer Workflow
Assists with learning through summaries, flashcards, and explanations

Features:
- Document summarization (structured hierarchical summaries)
- Flashcard generation (Anki-compatible format)
- Concept explanation (ELI5 style)
- Key term extraction
- Study plan generation

Usage:
    from workflows.study_summarizer import StudySummarizer

    summarizer = StudySummarizer()
    summary = summarizer.summarize_document(text, style="hierarchical")
    flashcards = summarizer.generate_flashcards(text, count=10)
"""

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import json


@dataclass
class Flashcard:
    """A study flashcard"""
    question: str
    answer: str
    tags: List[str] = field(default_factory=list)
    difficulty: str = "medium"  # easy, medium, hard
    source: Optional[str] = None


@dataclass
class KeyConcept:
    """A key concept extracted from text"""
    term: str
    definition: str
    related_terms: List[str] = field(default_factory=list)
    importance: str = "medium"  # low, medium, high


@dataclass
class StudySection:
    """A section of study material"""
    title: str
    content: str
    key_points: List[str] = field(default_factory=list)
    subsections: List["StudySection"] = field(default_factory=list)


class StudySummarizer:
    """
    Study Summarizer workflow for JARVIS.
    Provides tools for learning and study assistance.
    """

    # Common academic/technical terms to recognize
    SIGNAL_WORDS = {
        "definition": ["is defined as", "means", "refers to", "is called"],
        "example": ["for example", "such as", "for instance", "e.g."],
        "important": ["important", "key", "crucial", "essential", "note that"],
        "contrast": ["however", "but", "although", "whereas", "on the other hand"],
        "sequence": ["first", "second", "then", "next", "finally"],
        "cause_effect": ["because", "therefore", "thus", "as a result", "consequently"],
    }

    def __init__(self, workspace: Optional[str] = None):
        """
        Initialize Study Summarizer.

        Args:
            workspace: Directory for saving study materials
        """
        self.workspace = Path(workspace) if workspace else Path.cwd() / "study"
        self.workspace.mkdir(parents=True, exist_ok=True)

    def summarize_document(self, text: str, style: str = "hierarchical",
                          max_length: Optional[int] = None) -> str:
        """
        Generate a summary of the document.

        Args:
            text: The document text to summarize
            style: Summary style - "hierarchical", "bullet", "paragraph"
            max_length: Maximum summary length (approximate)

        Returns:
            Formatted summary
        """
        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        # Extract sections (look for headers)
        sections = self._extract_sections(text)

        # Identify key points
        key_points = self._extract_key_points(paragraphs)

        if style == "hierarchical":
            return self._format_hierarchical_summary(sections, key_points)
        elif style == "bullet":
            return self._format_bullet_summary(key_points)
        else:
            return self._format_paragraph_summary(key_points)

    def _extract_sections(self, text: str) -> List[StudySection]:
        """Extract document sections based on headers"""
        sections = []

        # Look for markdown headers or numbered sections
        header_pattern = r'^(?:#{1,3}\s+|\d+\.\s+)(.+)$'
        lines = text.split("\n")

        current_section = None
        current_content = []

        for line in lines:
            header_match = re.match(header_pattern, line)
            if header_match:
                # Save previous section
                if current_section:
                    current_section.content = "\n".join(current_content)
                    sections.append(current_section)

                # Start new section
                current_section = StudySection(
                    title=header_match.group(1).strip(),
                    content=""
                )
                current_content = []
            elif current_section:
                current_content.append(line)

        # Don't forget last section
        if current_section:
            current_section.content = "\n".join(current_content)
            sections.append(current_section)

        # If no sections found, treat whole text as one section
        if not sections:
            sections = [StudySection(title="Main Content", content=text)]

        return sections

    def _extract_key_points(self, paragraphs: List[str]) -> List[str]:
        """Extract key points from paragraphs"""
        key_points = []

        for para in paragraphs:
            # Look for sentences with importance signals
            sentences = re.split(r'[.!?]', para)

            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence or len(sentence) < 20:
                    continue

                # Check for importance signals
                has_signal = any(
                    signal in sentence.lower()
                    for signals in self.SIGNAL_WORDS.values()
                    for signal in signals
                )

                # Check for definitions
                if any(sig in sentence.lower() for sig in self.SIGNAL_WORDS["definition"]):
                    key_points.append(sentence)
                elif has_signal:
                    key_points.append(sentence)

        # Also extract first sentence of each paragraph (topic sentences)
        for para in paragraphs[:5]:  # Limit to first 5 paragraphs
            sentences = re.split(r'[.!?]', para)
            if sentences and sentences[0].strip():
                topic = sentences[0].strip()
                if topic not in key_points and len(topic) > 20:
                    key_points.insert(0, topic)

        return key_points[:15]  # Limit to 15 key points

    def _format_hierarchical_summary(self, sections: List[StudySection],
                                     key_points: List[str]) -> str:
        """Format as hierarchical summary"""
        summary = "# Summary\n\n"

        if sections:
            for section in sections:
                summary += f"## {section.title}\n\n"

                # Extract key points for this section
                section_points = []
                for point in key_points:
                    if point.lower() in section.content.lower():
                        section_points.append(point)

                if section_points:
                    for point in section_points[:3]:
                        summary += f"- {point}\n"
                else:
                    # Use first 100 chars as preview
                    preview = section.content[:200].strip()
                    if preview:
                        summary += f"{preview}...\n"
                summary += "\n"
        else:
            summary += "## Key Points\n\n"
            for point in key_points:
                summary += f"- {point}\n"

        return summary

    def _format_bullet_summary(self, key_points: List[str]) -> str:
        """Format as bullet point summary"""
        summary = "# Key Points Summary\n\n"
        for i, point in enumerate(key_points, 1):
            summary += f"{i}. {point}\n"
        return summary

    def _format_paragraph_summary(self, key_points: List[str]) -> str:
        """Format as paragraph summary"""
        summary = "# Summary\n\n"
        summary += " ".join(key_points[:5])
        return summary

    def generate_flashcards(self, text: str, count: int = 10,
                           format: str = "markdown") -> List[Flashcard]:
        """
        Generate flashcards from text.

        Args:
            text: Source text
            count: Number of flashcards to generate
            format: Output format - "markdown", "anki", "json"

        Returns:
            List of Flashcard objects
        """
        flashcards = []

        # Extract definitions
        definition_patterns = [
            r'(\w+(?:\s+\w+)?)\s+(?:is|are)\s+(?:defined as|called)\s+(.+?)[.!]',
            r'(\w+(?:\s+\w+)?)\s+(?:means|refers to)\s+(.+?)[.!]',
            r'(?:The|A|An)\s+(\w+(?:\s+\w+)?)\s+is\s+(.+?)[.!]',
        ]

        for pattern in definition_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                term = match.group(1).strip()
                definition = match.group(2).strip()

                if len(definition) > 10:  # Skip very short definitions
                    flashcards.append(Flashcard(
                        question=f"What is {term}?",
                        answer=definition,
                        tags=["definition"],
                        difficulty="medium"
                    ))

                if len(flashcards) >= count:
                    break
            if len(flashcards) >= count:
                break

        # Generate question-answer pairs from key sentences
        if len(flashcards) < count:
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            for para in paragraphs:
                sentences = re.split(r'[.!?]', para)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) < 30:
                        continue

                    # Convert statement to question
                    card = self._statement_to_flashcard(sentence)
                    if card:
                        flashcards.append(card)

                    if len(flashcards) >= count:
                        break
                if len(flashcards) >= count:
                    break

        return flashcards[:count]

    def _statement_to_flashcard(self, statement: str) -> Optional[Flashcard]:
        """Convert a statement into a flashcard"""
        # Look for patterns that can be converted to questions

        # Pattern: "X is Y" -> "What is X?"
        match = re.match(r'^(\w+(?:\s+\w+){0,3})\s+(?:is|are)\s+(.+)$', statement, re.IGNORECASE)
        if match:
            subject = match.group(1)
            predicate = match.group(2)
            return Flashcard(
                question=f"What is {subject}?",
                answer=f"{subject} is {predicate}",
                difficulty="easy"
            )

        # Pattern: "X causes Y" -> "What causes Y?"
        match = re.match(r'^(.+)\s+causes\s+(.+)$', statement, re.IGNORECASE)
        if match:
            cause = match.group(1)
            effect = match.group(2)
            return Flashcard(
                question=f"What causes {effect}?",
                answer=cause,
                difficulty="medium"
            )

        return None

    def format_flashcards(self, flashcards: List[Flashcard], format: str = "markdown") -> str:
        """
        Format flashcards for export.

        Args:
            flashcards: List of flashcards
            format: Output format - "markdown", "anki", "json"

        Returns:
            Formatted string
        """
        if format == "markdown":
            output = "# Flashcards\n\n"
            for i, card in enumerate(flashcards, 1):
                output += f"## Card {i}\n"
                output += f"**Q:** {card.question}\n\n"
                output += f"**A:** {card.answer}\n\n"
                if card.tags:
                    output += f"Tags: {', '.join(card.tags)}\n\n"
                output += "---\n\n"
            return output

        elif format == "anki":
            # Anki import format: front;back;tags
            lines = []
            for card in flashcards:
                front = card.question.replace(";", ",")
                back = card.answer.replace(";", ",")
                tags = " ".join(card.tags)
                lines.append(f"{front};{back};{tags}")
            return "\n".join(lines)

        elif format == "json":
            return json.dumps([
                {
                    "question": c.question,
                    "answer": c.answer,
                    "tags": c.tags,
                    "difficulty": c.difficulty
                }
                for c in flashcards
            ], indent=2)

        else:
            raise ValueError(f"Unknown format: {format}")

    def explain_concept(self, concept: str, text: str,
                       style: str = "simple") -> str:
        """
        Explain a concept from the text.

        Args:
            concept: The concept to explain
            text: The source text
            style: Explanation style - "simple", "eli5", "technical"

        Returns:
            Explanation text
        """
        # Find sentences mentioning the concept
        sentences = re.split(r'[.!?]', text)
        relevant = [s.strip() for s in sentences if concept.lower() in s.lower()]

        if not relevant:
            return f"Could not find information about '{concept}' in the text."

        explanation = f"# Understanding {concept}\n\n"

        # Find definition
        for sentence in relevant:
            if any(sig in sentence.lower() for sig in self.SIGNAL_WORDS["definition"]):
                explanation += f"## Definition\n{sentence}.\n\n"
                break

        # Find examples
        examples = [s for s in relevant
                   if any(sig in s.lower() for sig in self.SIGNAL_WORDS["example"])]
        if examples:
            explanation += "## Examples\n"
            for ex in examples[:3]:
                explanation += f"- {ex}\n"
            explanation += "\n"

        # Key points about the concept
        explanation += "## Key Points\n"
        for sentence in relevant[:5]:
            if sentence not in explanation:
                explanation += f"- {sentence}.\n"

        if style == "eli5":
            explanation += "\n## In Simple Terms\n"
            explanation += f"Think of {concept} as... [simplified analogy would be generated by LLM]\n"

        return explanation

    def extract_key_terms(self, text: str, limit: int = 20) -> List[KeyConcept]:
        """
        Extract key terms and their definitions from text.

        Args:
            text: Source text
            limit: Maximum number of terms

        Returns:
            List of key concepts
        """
        concepts = []

        # Look for definition patterns
        definition_patterns = [
            (r'(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b)\s+(?:is|are)\s+(?:defined as|called)\s+([^.]+)', "high"),
            (r'(?:The|A|An)\s+(\b[a-z]+(?:\s+[a-z]+)?\b)\s+is\s+([^.]+)', "medium"),
            (r'(\b[A-Z]{2,}\b)\s*[-:]\s*([^.]+)', "high"),  # Acronyms
        ]

        for pattern, importance in definition_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                term = match.group(1).strip()
                definition = match.group(2).strip()

                if len(term) > 2 and len(definition) > 10:
                    concepts.append(KeyConcept(
                        term=term,
                        definition=definition,
                        importance=importance
                    ))

                if len(concepts) >= limit:
                    break
            if len(concepts) >= limit:
                break

        return concepts

    def create_study_plan(self, text: str, study_time_hours: float = 2.0) -> str:
        """
        Create a study plan based on the material.

        Args:
            text: Study material
            study_time_hours: Available study time

        Returns:
            Study plan as markdown
        """
        sections = self._extract_sections(text)
        key_terms = self.extract_key_terms(text, limit=10)

        plan = f"""# Study Plan

**Estimated Time**: {study_time_hours} hours
**Date Generated**: {datetime.now().strftime("%Y-%m-%d")}

## Material Overview
- **Sections**: {len(sections)}
- **Key Terms**: {len(key_terms)}

## Recommended Approach

### Phase 1: Overview (15 min)
- Read through all section headers
- Skim the introduction and conclusion
- Identify main themes

### Phase 2: Deep Reading ({int(study_time_hours * 0.5 * 60)} min)
"""

        for i, section in enumerate(sections[:5], 1):
            time_per_section = int(study_time_hours * 0.5 * 60 / min(len(sections), 5))
            plan += f"- [ ] {section.title} (~{time_per_section} min)\n"

        plan += f"""
### Phase 3: Active Recall ({int(study_time_hours * 0.25 * 60)} min)
- Review flashcards generated from this material
- Try to explain concepts without looking
- Mark difficult concepts for review

### Phase 4: Review & Connect ({int(study_time_hours * 0.10 * 60)} min)
- Review marked difficult concepts
- Connect new knowledge to existing understanding
- Write brief summary in own words

## Key Terms to Master
"""

        for term in key_terms[:10]:
            plan += f"- [ ] **{term.term}**: {term.definition[:50]}...\n"

        plan += """
## Self-Assessment Questions
1. Can you explain the main concepts without notes?
2. Can you give an example for each key term?
3. How does this connect to what you already know?

---
*Good luck with your studies!*
"""

        return plan


# CLI interface
def main():
    """CLI for Study Summarizer"""
    import sys

    summarizer = StudySummarizer()

    if len(sys.argv) < 2:
        print("Usage: python study_summarizer.py [command]")
        print("Commands:")
        print("  summarize   - Summarize text from stdin")
        print("  flashcards  - Generate flashcards from stdin")
        print("  terms       - Extract key terms from stdin")
        print("  plan        - Create study plan from stdin")
        print("")
        print("Example:")
        print("  cat chapter.txt | python study_summarizer.py summarize")
        return

    command = sys.argv[1]
    text = sys.stdin.read()

    if command == "summarize":
        style = sys.argv[2] if len(sys.argv) > 2 else "hierarchical"
        print(summarizer.summarize_document(text, style=style))

    elif command == "flashcards":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        format_type = sys.argv[3] if len(sys.argv) > 3 else "markdown"
        cards = summarizer.generate_flashcards(text, count=count)
        print(summarizer.format_flashcards(cards, format=format_type))

    elif command == "terms":
        terms = summarizer.extract_key_terms(text)
        print("# Key Terms\n")
        for term in terms:
            print(f"**{term.term}** [{term.importance}]")
            print(f"  {term.definition}\n")

    elif command == "plan":
        hours = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
        print(summarizer.create_study_plan(text, study_time_hours=hours))

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
