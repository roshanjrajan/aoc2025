from __future__ import annotations
import argparse
from functools import reduce
import sys
from pathlib import Path
from tokenize import group


YEAR = 2025
ROOT = Path(__file__).resolve().parents[2]
DAY_DIR = Path(__file__).resolve().parent
DAY = DAY_DIR.name if DAY_DIR.name.startswith("day") else "dayXX"
DATA_DIR = ROOT / "data" / str(YEAR) / DAY
TESTS: list[tuple[str, int | str]] = [
    (
"""123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
""",3263827
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

def column(grouping: list[str]) -> list[int]:
    max_length:int = max([len(s) for s in grouping])
    out: list[int] = []
    for i in range(max_length):
        num = "".join([s[i] for s in grouping]).strip()
        if not num:
            continue
        out.append(int(num))

    return out

def solve(lines: list[str]) -> int | str:
    def add(a, b):
        return a + b
    def multiply(a, b):
        return a * b

    split_indexes: list[int] = []
    for i, char in enumerate(lines[0]):
        if char != " ":
            continue

        good = True
        for line in lines:
            if i < len(line) and line[i] != " ":
                good = False 

        if good:
            split_indexes.append(i)

    
    split_indexes.append(max([len(line) for line in lines]))
    groupings: list[list[str]] = []

    prev_idx = 0
    for idx in split_indexes:
        grouping: list[str] = []
        for line in lines[:-1]:
            grouping.append(line[prev_idx:min(idx, len(line))])
        groupings.append(grouping)
        prev_idx = idx

    output: list[int] = []
    for i, operator in enumerate(lines[-1].strip().split()):
        match operator:
            case "+":
                output.append(reduce(add, column(groupings[i])))
            case "*":
                output.append(reduce(multiply, column(groupings[i])))
            case _:
                print('operator not understood', operator) 
    
    return sum(output)

            


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
