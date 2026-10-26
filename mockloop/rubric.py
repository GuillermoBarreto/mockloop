"""Structured feedback on a candidate's spoken/written approach.

This is deliberately a transparent heuristic rubric, not a model judgment:
each criterion is a check the candidate can see, reproduce, and improve
against. A future version may add an optional LLM evaluator behind an
environment variable; the local rubric stays the default.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from mockloop.questions import Question

_APPROACH_WORDS = (
    "iterate", "loop", "scan", "hash", "map", "set", "pointer",
    "sort", "binary search", "recurs", "stack", "queue", "window",
    "two pointer", "divide", "brute force", "dictionary",
)

_EDGE_WORDS = (
    "empty", "null", "none", "duplicate", "single", "large",
    "sorted", "unsorted", "negative", "zero", "overflow",
)

_COMPLEXITY_RE = re.compile(r"O\([^)]+\)")


@dataclass(frozen=True)
class Criterion:
    name: str
    passed: bool
    note: str


@dataclass(frozen=True)
class Feedback:
    question_id: str
    score: float  # fraction of criteria passed, 0.0-1.0
    criteria: tuple[Criterion, ...]
    follow_up: str

    def passed_names(self) -> list[str]:
        return [c.name for c in self.criteria if c.passed]

    def missed_names(self) -> list[str]:
        return [c.name for c in self.criteria if not c.passed]


def evaluate_approach(question: Question, approach: str) -> Feedback:
    """Score an approach explanation against four visible criteria."""
    text = approach.lower()
    criteria = (
        Criterion(
            "approach",
            len(approach.strip()) >= 30
            and any(word in text for word in _APPROACH_WORDS),
            "Name the technique you would use (hash map, two pointers, sorting, ...).",
        ),
        Criterion(
            "complexity",
            bool(_COMPLEXITY_RE.search(approach)),
            "State time and space complexity, e.g. O(n) time and O(n) space.",
        ),
        Criterion(
            "edge_cases",
            any(word in text for word in _EDGE_WORDS),
            "Name at least one edge case (empty input, duplicates, a single element, ...).",
        ),
        Criterion(
            "test_cases",
            "test" in text or "example" in text or "e.g" in text,
            "Walk through a small example or name a test you would run.",
        ),
    )
    passed = sum(1 for criterion in criteria if criterion.passed)
    return Feedback(
        question_id=question.id,
        score=passed / len(criteria),
        criteria=criteria,
        follow_up=question.follow_up,
    )
