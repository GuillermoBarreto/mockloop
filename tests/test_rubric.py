"""Tests for the feedback rubric."""

import unittest

from mockloop.questions import find_question, load_bank
from mockloop.rubric import evaluate_approach

QUESTION = find_question(load_bank(), "two-sum")

STRONG = (
    "Iterate once with a hash map of values seen so far, checking for the "
    "complement on each step. That gives O(n) time and O(n) space. "
    "Edge cases: an empty array and duplicate values. "
    "Test it on [2, 7, 11, 15] with target 9, for example."
)


class TestRubric(unittest.TestCase):
    def test_strong_approach_scores_full_marks(self):
        feedback = evaluate_approach(QUESTION, STRONG)
        self.assertEqual(feedback.score, 1.0)
        self.assertEqual(feedback.missed_names(), [])
        self.assertTrue(feedback.follow_up)

    def test_empty_approach_scores_zero(self):
        feedback = evaluate_approach(QUESTION, "")
        self.assertEqual(feedback.score, 0.0)
        self.assertEqual(len(feedback.criteria), 4)

    def test_approach_without_complexity_misses_one_criterion(self):
        text = (
            "Iterate with a hash map and check complements. "
            "Edge cases: an empty array. Test on a small example."
        )
        feedback = evaluate_approach(QUESTION, text)
        self.assertEqual(feedback.score, 0.75)
        self.assertEqual(feedback.missed_names(), ["complexity"])

    def test_scores_stay_in_range(self):
        for text in ["hash", "O(n)", "empty test example hash map iterate"]:
            feedback = evaluate_approach(QUESTION, text)
            self.assertGreaterEqual(feedback.score, 0.0)
            self.assertLessEqual(feedback.score, 1.0)


if __name__ == "__main__":
    unittest.main()
