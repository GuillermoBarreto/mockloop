"""Tests for the question bank: loading, filtering, and picking."""

import unittest
from pathlib import Path

from mockloop.questions import (
    filter_questions,
    find_question,
    load_bank,
    pick_question,
)

BANK = load_bank()


class TestBank(unittest.TestCase):
    def test_bank_loads_eight_questions_with_unique_ids(self):
        self.assertEqual(len(BANK), 8)
        self.assertEqual(len({q.id for q in BANK}), 8)

    def test_filter_by_topic(self):
        hashes = filter_questions(BANK, topic="hash-maps")
        self.assertEqual(len(hashes), 4)
        self.assertTrue(all(q.topic == "hash-maps" for q in hashes))

    def test_filter_by_difficulty(self):
        medium = filter_questions(BANK, difficulty="medium")
        self.assertEqual(len(medium), 4)

    def test_seeded_pick_is_reproducible(self):
        first = pick_question(BANK, topic="two-pointers", seed=7)
        second = pick_question(BANK, topic="two-pointers", seed=7)
        self.assertEqual(first.id, second.id)

    def test_pick_with_no_match_raises(self):
        with self.assertRaises(ValueError):
            pick_question(BANK, topic="graphs")

    def test_find_unknown_id_raises(self):
        with self.assertRaises(ValueError):
            find_question(BANK, "not-a-question")

    def test_custom_bank_file_loads(self):
        custom = Path(__file__).with_name("custom_bank.json")
        custom.write_text(
            '[{"id": "demo", "title": "Demo", "topic": "arrays", '
            '"difficulty": "easy", "prompt": "Do a demo.", "hints": [], '
            '"edge_cases": [], "follow_up": "None."}]',
            encoding="utf-8",
        )
        try:
            questions = load_bank(custom)
            self.assertEqual([q.id for q in questions], ["demo"])
        finally:
            custom.unlink()


if __name__ == "__main__":
    unittest.main()
