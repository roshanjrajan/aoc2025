# aoc2025

## Useful commands
- Fetch input: `uv run main.py fetch --year 2025 --day <n>`
- Execute a solution: `uv run main.py execute --day <n> --part <1|2>`
- Execute inline tests for a solution (requires `run_tests()` in the file): `uv run main.py execute --day <n> --part <1|2> --test`
- Copy part1 to part2 for a day: `uv run main.py copy-part --day <n> [--force]` (executing part 2 will auto-bootstrap if missing)
- Automatically sync part2 from part1 while you edit: `uv run main.py sync-part2 --day <n> [--interval 1.0]`

## Adding inline tests to a solution
Each `solutions/dayXX/partY.py` file has a `TESTS` list and `run_tests()` helper. Paste example input/expected pairs like:
```python
TESTS = [
    (
        """R2
        L3""",
        5,
    ),
]
```
Run them with `uv run main.py execute --day 1 --part 1 --test` or `uv run solutions/day01/part1.py --test`.
