from __future__ import annotations
from cgi import test

"""
Template for new Advent of Code solutions.

Copy this file into solutions/dayXX/part1.py (and part2.py) before editing.
Update YEAR if you are working on a different event.
"""

import argparse
import sys
from pathlib import Path


YEAR = 2025
ROOT = Path(__file__).resolve().parents[2]
DAY_DIR = Path(__file__).resolve().parent
DAY = DAY_DIR.name if DAY_DIR.name.startswith("day") else "dayXX"
DATA_DIR = ROOT / "data" / str(YEAR) / DAY
TESTS: list[tuple[str, int | str]] = [
    (
        """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124""",
1227775554
    ),
    (
        "580816-616131",
        0
    )
]


def read_input() -> list[str]:
    """
    Load the puzzle input for this part.

    Only one input file is stored (part1.txt).
    """
    part1 = DATA_DIR / "part1.txt"

    if not part1.exists():
        raise FileNotFoundError(f"No input file found in {DATA_DIR}. Add part1.txt.")

    return part1.read_text().splitlines()

def get_invalid_ids(start: str, end: str) -> set[str]:
    invalid_keys = set()
    # Check for both are odd with same digits
    if len(start) % 2 == 1 and len(end) % 2 == 1 and len(start) == len(end):
        return invalid_keys 

    if len(start) % 2 == 1:
        start = '1' + '0'*len(start)
    
    if len(end) % 2 == 1:
        end = '9'*(len(end) - 1)

    start_i = int(start)
    end_i = int(end)

    if start > end:
        return invalid_keys
    
    length = len(start) // 2
    digits = start[:length]

    while 1:
        curr = int(digits + digits)
        if start_i <= curr <= end_i:
            invalid_keys.add(curr)
            digits = str(int(digits) + 1)
        elif curr <= end_i:
            digits = str(int(digits) + 1)
        else:
            break
    return invalid_keys

def solve(lines: list[str]) -> int | str:
    """Implement the solution for this part."""
    all_ranges: list[tuple[str, str]] = []
    invalid_ids = set[str]()
    print(lines)
    for line in lines:
        ranges = line.split(",")
        for curr_range in ranges:
            start, end = curr_range.split('-')
            all_ranges.append((start, end))

    for curr_range in all_ranges:
        new_invalid_ids = get_invalid_ids(curr_range[0], curr_range[1])
        print(curr_range, new_invalid_ids)
        invalid_ids = invalid_ids.union(new_invalid_ids)

    return sum(map(int, invalid_ids))


def run_tests() -> None:
    if not TESTS:
        raise SystemExit("Add test cases to TESTS to run tests.")

    failed = False
    for idx, (raw, expected) in enumerate(TESTS, start=1):
        lines = [line for line in raw.strip().splitlines() if line.strip()]
        result = solve(lines)

        if result != expected:
            failed = True
            print(f"Test {idx} failed: expected {expected!r}, got {result!r}")
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
