from __future__ import annotations
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
"""3-5
10-14
16-20
12-18

1
5
8
11
17
32
""",14
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

def solve(lines: list[str]) -> int | str:
    idx = 0
    intervals: list[tuple[int, int]] = []
    while lines[idx].strip() and idx < len(lines):
        start, end = lines[idx].split("-")
        idx += 1
        intervals.append((int(start), int(end)))

    
    intervals.sort()
    merged_intervals: list[tuple[int, int]] = []

    for interval in intervals:
        if not merged_intervals:
            merged_intervals.append(interval)
        
        m_s, m_e = merged_intervals[-1]
        i_s, i_e = interval

        if m_s <= i_s <= m_e:
            merged_intervals[-1] = (m_s, max(i_e, m_e))
        else:
            merged_intervals.append(interval)

    length = 0
    for (start, end) in merged_intervals:
        length += end - start + 1
    
    return length

def run_tests() -> None:
    if not TESTS:
        raise SystemExit("Add test cases to TESTS to run tests.")

    failed = False
    for idx, (raw, expected) in enumerate(TESTS, start=1):
        lines = [line for line in raw.strip().splitlines()]
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
