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
"""987654321111111
811111111111119
234234234234278
818181911112111
""",357
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
    """Implement the solution for this part.""" 
    total = 0
    print(lines)
    for line in lines:
        curr_max = 0
        first: int = int(line[0])
        second:int = int(line[1])

        for i in range(2, len(line)):
            line_i_int = int(line[i])
            if line_i_int > second:
                second = line_i_int

            if line_i_int > first:
                curr_max = max(curr_max, int(str(first) + str(second)))
                if i + 1 < len(line):
                    first, second = int(line[i]), int(line[i+1])


        curr_max = max(curr_max, int(str(first) + str(second)))
        total += curr_max
        print(line, curr_max)
    
    return total



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
