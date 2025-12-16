from __future__ import annotations

import argparse
import math
import sys

from pathlib import Path


# Resolve project root from this file's location.
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "2025" / "day01"
TESTS: list[tuple[str, int | str]] = [(
"""L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""",
6
),
( # 50 -> 0, 0 -> 50, 0, 0 -> 0
"""L200
L150
L100
""",
5
),
( # 50 -> 0, 0 -> 50, 0, 0 -> 0
"""L50
R688
""",
7
)
]


def read_input() -> list[str]:
    """
    Load the puzzle input for part 1.

    This defaults to part1.txt (as downloaded by main.py fetch).
    """
    path = DATA_DIR / "part1.txt"
    return path.read_text().splitlines()



def solve(lines: list[str]) -> str | int:
    """
    Implement the actual Part 1 solution here.

    Replace the NotImplementedError with your solution logic.
    """

    pos = 50
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        direction = line[0]
        distance = int(line[1:])

        total += count_hits_to_zero(pos, direction, distance)

        if direction == "R":
            pos = (pos + distance) % 100
        else:
            pos = (pos - distance) % 100

    return total


def count_hits_to_zero(pos: int, direction: str, distance: int) -> int:
    if direction == "R":
        first_zero = (100 - pos) % 100
    else:  
        first_zero = pos % 100

    if first_zero == 0:
        # Require at least one click to "cause" a landing on 0
        first_zero = 100

    if distance < first_zero:
        return 0
    return 1 + (distance - first_zero) // 100


def run_tests() -> None:
    if not TESTS:
        raise SystemExit("Add test cases to TESTS to run tests.")

    failed = False
    for idx, (raw, expected) in enumerate(TESTS, start=1):
        print(f'\n\nRunning Test {idx}')
        lines = [line for line in raw.strip().splitlines() if line.strip()]
        result = solve(lines)
        if result != expected:
            failed = True
            print(f"Test {idx} failed: expected {expected!r}, got {result!r}")
    if not failed:
        print(f"All tests passed")


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Day 1 Part 1")
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
