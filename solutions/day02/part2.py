from __future__ import annotations
from dataclasses import dataclass
import json
from typing import Any
from cgi import test
import math
import pydantic

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
4174379265
    ),
    (
        "1-1000000000",
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
    start_i = int(start)
    end_i = int(end)

    if start_i > end_i:
        return invalid_keys

    if len(start) != len(end):
        curr_start = start
        for i in range(len(start), len(end) + 1):
            curr_end  = "9"* i
            if int(curr_end) > end_i:
                curr_end = end

            invalid_keys = invalid_keys.union(get_invalid_ids(curr_start, curr_end))
            curr_start = "1" + "0"*i
        
        return invalid_keys
        

    # Assume lengths are the same
    checks = 0
    for digit_length in range(1, len(end) // 2 + 1):
        if len(start) % digit_length != 0:
            continue

        digits = start[:digit_length]

        while 1:
            # breakpoint()
            if len(digits) != digit_length:
                break

            curr = int(digits*(len(start)//digit_length))
            checks += 1
            if start_i <= curr <= end_i:
                invalid_keys.add(curr)
                digits = str(int(digits) + 1)
            elif curr <= end_i:
                digits = str(int(digits) + 1)
            else:
                break
    # print(checks, start, end)
        
    return invalid_keys

def factors(N: int):
    output: list[int] = []
    for i in range(1, N + 1):
        if N % i == 0:
            output.extend([i, N // i])
    
    return sorted(set(output))


class PrecomputedValues(pydantic.BaseModel):
    computed_n: int = 1
    computed_keys: list[int] = []

def precompute_values(max_digit_length: int, data: str | None) -> PrecomputedValues:
    if data:
        values = PrecomputedValues.model_validate_json(data or '')
    else:
        values = PrecomputedValues()

    computed_n: int = values.computed_n


    start = str(max(1, computed_n))
    end = str(int("9"*max_digit_length))

    if end <= start:
        return values

    new_keys: set[int] = set(map(int, get_invalid_ids(start, end)))
    values.computed_keys = sorted(set(values.computed_keys).union(new_keys))
    values.computed_n = int(end)

    with open(DATA_DIR / 'invalid_keys.json', 'w') as f:
        f.write(values.model_dump_json())

    return values


def fetch_precomputed_values(n: int) -> list[int]:
    with open(DATA_DIR / 'invalid_keys.json') as f:
        data = f.read()
    
    return precompute_values(n, data).computed_keys

def solve2(lines: list[str]) -> int | str:
    all_ranges: list[tuple[str, str]] = []
    invalid_ids = set[int]()
    for line in lines:
        ranges = line.split(",")
        for curr_range in ranges:
            start, end = curr_range.split('-')
            all_ranges.append((start, end))
        
    max_length = 0
    for r in all_ranges:
        max_length = max(max_length, len(r[0]), len(r[1]))

    precomputed_values = set(fetch_precomputed_values(max_length))

    for r in all_ranges:
        start, end = r
        for i in range(int(start), int(end) + 1):
            if i in precomputed_values:
                invalid_ids.add(i)

    return sum(invalid_ids)


def solve(lines: list[str]) -> int | str:
    """Implement the solution for this part."""
    all_ranges: list[tuple[str, str]] = []
    invalid_ids = set[str]()
    for line in lines:
        ranges = line.split(",")
        for curr_range in ranges:
            start, end = curr_range.split('-')
            all_ranges.append((start, end))

    for curr_range in all_ranges:
        new_invalid_ids = get_invalid_ids(curr_range[0], curr_range[1])
        # print(curr_range, sorted(new_invalid_ids))
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
