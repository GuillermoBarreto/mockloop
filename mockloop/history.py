"""Practice history: append-only JSONL records and simple summaries."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from mockloop.rubric import Feedback


def append_record(path: Path, question_topic: str, feedback: Feedback) -> None:
    """Append one evaluation record (one JSON object per line)."""
    record = {
        "question_id": feedback.question_id,
        "topic": question_topic,
        "score": feedback.score,
        "passed": feedback.passed_names(),
        "missed": feedback.missed_names(),
    }
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def summarize(path: Path) -> dict:
    """Summarise a history file; an absent file counts as zero sessions."""
    if not path.exists():
        return {"sessions": 0, "average_score": 0.0, "by_topic": {}}
    records = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    if not records:
        return {"sessions": 0, "average_score": 0.0, "by_topic": {}}
    average = sum(record["score"] for record in records) / len(records)
    return {
        "sessions": len(records),
        "average_score": round(average, 3),
        "by_topic": dict(Counter(record["topic"] for record in records)),
    }
