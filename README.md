# Mockloop

A small CLI mock-interview coach. It picks a data-structures question from a
local bank, and scores an approach explanation against four visible criteria:
does it name a technique, state the complexity, name an edge case, and walk
through a test or example.

## Why

Interview feedback is usually vague ("be more structured"). Mockloop makes the
structure explicit: every criterion is a check you can see, reproduce, and
improve against, and every question ships with hints, edge cases, and a
follow-up question.

## Install

Python 3.11+ only, no third-party dependencies:

```sh
git clone https://github.com/GuillermoBarreto/mockloop.git
cd mockloop
```

## Usage

List the question bank, filtered by topic or difficulty:

```sh
python -m mockloop.cli list --topic hash-maps
python -m mockloop.cli list --difficulty medium
```

Ask a question (add `--seed 7` for a reproducible pick):

```sh
python -m mockloop.cli ask --topic two-pointers --seed 7
python -m mockloop.cli ask --id two-sum
```

Score an approach explanation:

```sh
python -m mockloop.cli evaluate --id two-sum --approach \
  "Iterate once with a hash map of values seen so far. That gives O(n) time \
   and O(n) space. Edge cases: an empty array and duplicate values. \
   Test it on [2, 7, 11, 15] with target 9, for example."
```

Keep a practice history (JSONL, one record per session) and summarise it:

```sh
python -m mockloop.cli evaluate --id two-sum --approach "..." \
  --history sessions.jsonl
python -m mockloop.cli stats --history sessions.jsonl
```

## How the rubric works

The starter rubric is keyword-based and runs entirely locally — no network
calls, no API keys, no model judgment. It is a structure check, not a
correctness proof: a high score means the explanation covered the four
criteria, not that the algorithm is right. See `mockloop/rubric.py` for the
exact checks.

## Questions

The bank in `mockloop/questions.json` covers arrays, hash maps, two pointers,
and strings — the patterns that come up most in technical interviews. Each
entry has a prompt, hints, edge cases, and a follow-up question.

## Tests

```sh
python -m unittest discover -s tests -v
```

## Roadmap

- Optional LLM evaluator behind an environment variable (local rubric stays default)
- Timed practice sessions and per-topic progress reports
- More question topics (graphs, dynamic programming, system design prompts)
- A question-contribution format so new questions can be added as JSON

## License

MIT. See `LICENSE`.
