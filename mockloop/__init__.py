"""Mockloop: a small CLI mock-interview coach.

Pick a data-structures question from a local bank, practise explaining an
approach, and get structured, explainable feedback on that explanation.
No network calls and no paid API: the starter feedback rubric is keyword
based and runs entirely locally.
"""

from mockloop.questions import Question, load_bank, pick_question
from mockloop.rubric import Feedback, evaluate_approach

__version__ = "0.1.0"

__all__ = ["Question", "Feedback", "load_bank", "pick_question", "evaluate_approach", "__version__"]
