"""Tests for the CLI and the history summary, via subprocess."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "mockloop.cli", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class TestCli(unittest.TestCase):
    def test_list_shows_questions(self):
        result = run_cli("list")
        self.assertEqual(result.returncode, 0)
        self.assertIn("two-sum", result.stdout)

    def test_list_with_topic_filter(self):
        result = run_cli("list", "--topic", "two-pointers")
        self.assertEqual(result.returncode, 0)
        self.assertIn("two-sum-ii", result.stdout)
        self.assertNotIn("valid-anagram", result.stdout)

    def test_ask_specific_question(self):
        result = run_cli("ask", "--id", "two-sum")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Two Sum", result.stdout)
        self.assertIn("target", result.stdout)

    def test_ask_unknown_id_fails(self):
        result = run_cli("ask", "--id", "nope")
        self.assertNotEqual(result.returncode, 0)

    def test_evaluate_and_stats_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            history_path = Path(tmp) / "sessions.jsonl"
            result = run_cli(
                "evaluate",
                "--id", "two-sum",
                "--approach",
                "Iterate with a hash map, O(n) time. Edge cases: empty input. "
                "Test on a small example.",
                "--history", str(history_path),
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Score: 1.00", result.stdout)
            record = json.loads(history_path.read_text(encoding="utf-8").strip())
            self.assertEqual(record["question_id"], "two-sum")

            stats = run_cli("stats", "--history", str(history_path))
            self.assertEqual(stats.returncode, 0)
            self.assertIn("Sessions: 1", stats.stdout)
            self.assertIn("Average score: 1.000", stats.stdout)

    def test_stats_on_missing_file_is_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            stats = run_cli("stats", "--history", str(Path(tmp) / "missing.jsonl"))
            self.assertEqual(stats.returncode, 0)
            self.assertIn("Sessions: 0", stats.stdout)


if __name__ == "__main__":
    unittest.main()
