from __future__ import annotations
import enum
import argparse
import sys
import itertools

from typing import Generator
from pathlib import Path


YEAR = 2025
ROOT = Path(__file__).resolve().parents[2]
DAY_DIR = Path(__file__).resolve().parent
DAY = DAY_DIR.name if DAY_DIR.name.startswith("day") else "dayXX"
DATA_DIR = ROOT / "data" / str(YEAR) / DAY
TESTS: list[tuple[str, int | str]] = [
(
"""..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""", 13
)
]

EXPECTED = """..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
"""


def read_input() -> list[str]:
    """
    Load the puzzle input for this part.

    Only one input file is stored (part1.txt).
    """
    part1 = DATA_DIR / "part1.txt"

    if not part1.exists():
        raise FileNotFoundError(f"No input file found in {DATA_DIR}. Add part1.txt.")

    return part1.read_text().splitlines()

def neighbors(r: int, c: int) -> Generator[tuple[int, int]]:
    for dir_r, dir_c in itertools.product([-1, 0, 1], repeat=2):
        if dir_r == 0 and dir_c == 0:
            continue
        yield (r + dir_r, c + dir_c)

def print_grid(grid: list[list[str]]):
    print()
    print("\n".join(["".join(row) for row in grid]))

def solve(lines: list[str]) -> int | str:
    total = 0
    all_removed = set[tuple[int, int]]()
    all_possible= set[tuple[int, int]]()
    for line_r, line_val in enumerate(lines):
        for line_c, cell_val in enumerate(line_val):
            if cell_val == '@':
                all_possible.add((line_r, line_c))
    
    while True:
        removed = set[tuple[int, int]]()
        for (r, c) in all_possible:
            count = 0
            for n_r, n_c in neighbors(r, c):
                if (n_r, n_c) in all_possible:
                    count += 1
            if count < 4:
                removed.add((r, c))
        if not removed:
            break

        all_possible = all_possible.difference(removed)
        all_removed.update(removed)
    
    return len(all_removed)

def run_tests() -> None:
    if not TESTS:
        raise SystemExit("Add test cases to TESTS to run tests.")

    failed = False
    for idx, (raw, expected) in enumerate(TESTS, start=1):
        lines = [line for line in raw.strip().splitlines() if line.strip()]
        result = solve(lines)

        if result != expected:
            failed = True
            print(f"Test {idx} failed: expected {expected!r}, got {result!r}\n\n")
        else:
            print(f"Test {idx} passed: got {result!r}\n\n")
    
    if not failed:
        print(f"All {len(TESTS)} tests passed.")


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Advent of Code solver template. Copy into day folder before editing."
    )
    parser.add_argument(
        "--test", action="store_true", help="Run inline TESTS instead of puzzle input"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_cli(argv or sys.argv[1:])
    if args.test:
        run_tests()
        return

    lines = read_input()
    answer = solve(lines)
    print(answer)


if __name__ == "__main__":
    main()
