"""Command line interface for mockloop.

Usage examples (run from the repository root):

    python -m mockloop.cli list --topic hash-maps
    python -m mockloop.cli ask --topic two-pointers --seed 7
    python -m mockloop.cli evaluate --id two-sum --approach "Use a hash map ..."
    python -m mockloop.cli stats --history sessions.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from mockloop import history, load_bank
from mockloop.questions import find_question, pick_question
from mockloop.rubric import evaluate_approach


def _list(args: argparse.Namespace) -> int:
    from mockloop.questions import filter_questions

    questions = filter_questions(load_bank(), topic=args.topic, difficulty=args.difficulty)
    if not questions:
        print("no questions match that filter", file=sys.stderr)
        return 1
    for question in questions:
        print(f"{question.id} — {question.title} [{question.topic}, {question.difficulty}]")
    return 0


def _ask(args: argparse.Namespace) -> int:
    try:
        if args.id:
            question = find_question(load_bank(), args.id)
        else:
            question = pick_question(
                load_bank(), topic=args.topic, difficulty=args.difficulty, seed=args.seed
            )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"{question.title} [{question.topic}, {question.difficulty}]")
    print()
    print(question.prompt)
    print()
    print("Hints:")
    for hint in question.hints:
        print(f"  - {hint}")
    return 0


def _evaluate(args: argparse.Namespace) -> int:
    try:
        question = find_question(load_bank(), args.id)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    feedback = evaluate_approach(question, args.approach)
    print(f"Score: {feedback.score:.2f} ({len(feedback.passed_names())}/4 criteria)")
    for criterion in feedback.criteria:
        mark = "pass" if criterion.passed else "miss"
        print(f"  [{mark}] {criterion.name}: {criterion.note}")
    print(f"Follow-up: {feedback.follow_up}")
    if args.history:
        history.append_record(Path(args.history), question.topic, feedback)
    if args.json:
        print(json.dumps({"question_id": question.id, "score": feedback.score}))
    return 0


def _stats(args: argparse.Namespace) -> int:
    summary = history.summarize(Path(args.history))
    print(f"Sessions: {summary['sessions']}")
    print(f"Average score: {summary['average_score']:.3f}")
    for topic, count in sorted(summary["by_topic"].items()):
        print(f"  {topic}: {count}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mockloop", description="Mock-interview coach")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="list questions in the bank")
    list_parser.add_argument("--topic")
    list_parser.add_argument("--difficulty")
    list_parser.set_defaults(func=_list)

    ask_parser = sub.add_parser("ask", help="show one interview question")
    ask_parser.add_argument("--id", help="ask a specific question id")
    ask_parser.add_argument("--topic")
    ask_parser.add_argument("--difficulty")
    ask_parser.add_argument("--seed", type=int, help="make the pick reproducible")
    ask_parser.set_defaults(func=_ask)

    eval_parser = sub.add_parser("evaluate", help="score an approach explanation")
    eval_parser.add_argument("--id", required=True)
    eval_parser.add_argument("--approach", required=True)
    eval_parser.add_argument("--history", help="append this session to a JSONL file")
    eval_parser.add_argument("--json", action="store_true")
    eval_parser.set_defaults(func=_evaluate)

    stats_parser = sub.add_parser("stats", help="summarise a history file")
    stats_parser.add_argument("--history", required=True)
    stats_parser.set_defaults(func=_stats)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
