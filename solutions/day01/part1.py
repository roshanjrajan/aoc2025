from __future__ import annotations

import argparse
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
3
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
    count = 0
    for line in lines:
        match line[0]:
            case "L":
                pos -= int(line[1:])
            case "R":
                pos += int(line[1:])
        if pos < 0:
            pos = pos % 100 
        if pos > 99:
            pos = pos % 100
        if pos == 0:
            count += 1
    return count


def run_tests() -> None:
    if not TESTS:
        raise SystemExit("Add test cases to TESTS to run tests.")

    for idx, (raw, expected) in enumerate(TESTS, start=1):
        lines = [line for line in raw.strip().splitlines() if line.strip()]
        result = solve(lines)
        if result != expected:
            raise AssertionError(
                f"Test {idx} failed: expected {expected!r}, got {result!r}"
            )
    print(f"All {len(TESTS)} tests passed.")


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
