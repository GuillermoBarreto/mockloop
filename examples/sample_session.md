# Sample session (synthetic transcript)

```sh
$ python -m mockloop.cli ask --id two-sum
Two Sum [hash-maps, easy]

Given an array of integers and a target, return the indices of the two
numbers that add up to the target. Assume exactly one solution exists.

Hints:
  - A single pass can remember what you have already seen.
  - What lookup structure gives you O(1) checks?

$ python -m mockloop.cli evaluate --id two-sum --approach \
    "Iterate once with a hash map of values seen so far. That gives O(n) \
     time and O(n) space. Edge cases: an empty array and duplicate values. \
     Test it on [2, 7, 11, 15] with target 9, for example."
Score: 1.00 (4/4 criteria)
  [pass] approach: Name the technique you would use (hash map, two pointers, sorting, ...).
  [pass] complexity: State time and space complexity, e.g. O(n) time and O(n) space.
  [pass] edge_cases: Name at least one edge case (empty input, duplicates, a single element, ...).
  [pass] test_cases: Walk through a small example or name a test you would run.
Follow-up: How would your approach change if the array were sorted?
```
