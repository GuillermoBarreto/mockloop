"""The local question bank: loading, filtering, and picking questions."""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path

_BANK_PATH = Path(__file__).with_name("questions.json")


@dataclass(frozen=True)
class Question:
    """One mock-interview question."""

    id: str
    title: str
    topic: str
    difficulty: str
    prompt: str
    hints: tuple[str, ...]
    edge_cases: tuple[str, ...]
    follow_up: str


def _from_record(record: dict) -> Question:
    return Question(
        id=record["id"],
        title=record["title"],
        topic=record["topic"],
        difficulty=record["difficulty"],
        prompt=record["prompt"],
        hints=tuple(record.get("hints", [])),
        edge_cases=tuple(record.get("edge_cases", [])),
        follow_up=record.get("follow_up", ""),
    )


def load_bank(path: Path | None = None) -> list[Question]:
    """Load every question from the bundled bank (or ``path`` if given)."""
    source = path or _BANK_PATH
    with open(source, encoding="utf-8") as handle:
        records = json.load(handle)
    questions = [_from_record(record) for record in records]
    ids = [question.id for question in questions]
    if len(ids) != len(set(ids)):
        raise ValueError("question bank has duplicate ids")
    return questions


def filter_questions(
    questions: list[Question],
    topic: str | None = None,
    difficulty: str | None = None,
) -> list[Question]:
    """Return the questions matching the given topic and/or difficulty."""
    result = questions
    if topic is not None:
        result = [q for q in result if q.topic == topic]
    if difficulty is not None:
        result = [q for q in result if q.difficulty == difficulty]
    return result


def pick_question(
    questions: list[Question],
    topic: str | None = None,
    difficulty: str | None = None,
    seed: int | None = None,
) -> Question:
    """Pick one matching question; ``seed`` makes the pick reproducible."""
    matches = filter_questions(questions, topic=topic, difficulty=difficulty)
    if not matches:
        raise ValueError("no question matches that topic/difficulty")
    if seed is not None:
        return random.Random(seed).choice(matches)
    return random.choice(matches)


def find_question(questions: list[Question], question_id: str) -> Question:
    """Return the question with ``question_id`` or raise ``ValueError``."""
    for question in questions:
        if question.id == question_id:
            return question
    raise ValueError(f"unknown question id: {question_id}")
