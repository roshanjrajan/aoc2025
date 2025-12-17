from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import hashlib
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
SOLUTIONS_DIR = ROOT / "solutions"
ENV_PATH = ROOT / ".env"
AOC_COOKIE_KEY = "AOC_COOKIE"


def load_env(path: Path = ENV_PATH) -> Dict[str, str]:
    """
    Load environment variables from .env (if present) without clobbering existing
    environment values.
    """
    load_dotenv(path, override=False)
    return {key: os.environ[key] for key in os.environ if key == AOC_COOKIE_KEY}


def get_cookie(explicit_cookie: Optional[str]) -> str:
    load_env()
    cookie = explicit_cookie or os.environ.get(AOC_COOKIE_KEY)
    if not cookie:
        raise SystemExit(
            f"Missing cookie: provide --cookie or set {AOC_COOKIE_KEY} in .env/env."
        )
    return cookie


def fetch_input(day: int, year: int, cookie: str) -> Path:
    if day < 1 or day > 25:
        raise SystemExit("Day must be between 1 and 25.")

    day_dir = DATA_DIR / str(year) / f"day{day:02d}"
    day_dir.mkdir(parents=True, exist_ok=True)
    target_path = day_dir / "part1.txt"

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    try:
        resp = requests.get(
            url,
            headers={"Cookie": cookie, "User-Agent": "aoc-cli"},
            timeout=15,
        )
    except requests.RequestException as exc:
        raise SystemExit(f"Network error fetching day {day}: {exc}")

    if resp.status_code != 200:
        raise SystemExit(
            f"HTTP error {resp.status_code} fetching day {day}: {resp.text.strip()}"
        )

    target_path.write_bytes(resp.content)
    print(f"Wrote input to {target_path.relative_to(ROOT)}")
    return target_path


def bootstrap_solution_file(day: int, year: int) -> Path:
    """Create part1.py for a day from the template if it does not already exist."""
    if day < 1 or day > 25:
        raise SystemExit("Day must be between 1 and 25.")

    day_dir = SOLUTIONS_DIR / f"day{day:02d}"
    dest = day_dir / "part1.py"
    if dest.exists():
        return dest

    template = SOLUTIONS_DIR / "template.py"
    if not template.exists():
        raise SystemExit(
            f"Template not found: {template.relative_to(ROOT)}. "
            "Add solutions/template.py to enable bootstrapping."
        )

    day_dir.mkdir(parents=True, exist_ok=True)
    content = template.read_text()
    content = content.replace("YEAR = 2025", f"YEAR = {year}")
    dest.write_text(content)
    print(f"Bootstrapped {dest.relative_to(ROOT)} from template.")
    return dest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Advent of Code helper CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch_parser = subparsers.add_parser("fetch", help="Fetch puzzle input")
    fetch_parser.add_argument("--day", type=int, required=True, help="Day number (1-25)")
    fetch_parser.add_argument(
        "--year",
        type=int,
        default=dt.datetime.now().year,
        help="Year (default: current year)",
    )
    fetch_parser.add_argument(
        "--cookie",
        type=str,
        help="Cookie string to override AOC_COOKIE env/.env",
    )

    execute_parser = subparsers.add_parser(
        "execute",
        help="Run a specific solution (or its inline tests) by day and part",
    )
    execute_parser.add_argument(
        "--day",
        type=int,
        required=True,
        help="Day number (1-25)",
    )
    execute_parser.add_argument(
        "--part",
        type=int,
        choices=[1, 2],
        required=True,
        help="Puzzle part (1 or 2)",
    )
    execute_parser.add_argument(
        "--test",
        action="store_true",
        help="Run inline tests (requires run_tests in the solution file)",
    )

    sync_parser = subparsers.add_parser(
        "sync-part2",
        help="Watch part1.py for a day and sync changes into part2.py until interrupted",
    )
    sync_parser.add_argument(
        "--day",
        type=int,
        required=True,
        help="Day number (1-25)",
    )
    sync_parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Polling interval in seconds (default: 1.0)",
    )

    copy_parser = subparsers.add_parser(
        "copy-part", help="Copy part1.py to part2.py for a given day"
    )
    copy_parser.add_argument("--day", type=int, required=True, help="Day number (1-25)")
    copy_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite part2.py if it already exists",
    )
    return parser.parse_args()


def load_solution_module(day: int, part: int):
    if day < 1 or day > 25:
        raise SystemExit("Day must be between 1 and 25.")
    path = SOLUTIONS_DIR / f"day{day:02d}" / f"part{part}.py"

    if part == 2 and not path.exists():
        copy_part_one_to_two(day=day, force=True)

    if not path.exists():
        raise SystemExit(f"Solution file not found: {path.relative_to(ROOT)}")

    module_name = f"solutions.day{day:02d}.part{part}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load module from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_solution(day: int, part: int, run_tests: bool) -> None:
    module = load_solution_module(day, part)

    if run_tests:
        run_tests_fn = getattr(module, "run_tests", None)
        if not callable(run_tests_fn):
            raise SystemExit(
                f"{module.__file__} missing run_tests(). Add run_tests() to the solution file."
            )
        run_tests_fn()
        return

    read_input = getattr(module, "read_input", None)
    solve = getattr(module, "solve", None)
    if not callable(read_input) or not callable(solve):
        raise SystemExit(
            f"{module.__file__} must define read_input() and solve(lines) to execute."
        )

    lines = read_input()
    result = solve(lines)
    print(result)


def copy_part_one_to_two(day: int, force: bool) -> None:
    if day < 1 or day > 25:
        raise SystemExit("Day must be between 1 and 25.")
    day_dir = SOLUTIONS_DIR / f"day{day:02d}"
    src = day_dir / "part1.py"
    dest = day_dir / "part2.py"
    if not src.exists():
        raise SystemExit(f"Source file not found: {src.relative_to(ROOT)}")
    if dest.exists() and not force:
        raise SystemExit(
            f"{dest.relative_to(ROOT)} already exists. Re-run with --force to overwrite."
        )
    day_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dest)
    print(f"Copied {src.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")


def file_hash(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def sync_part_two(day: int, interval: float) -> None:
    if day < 1 or day > 25:
        raise SystemExit("Day must be between 1 and 25.")
    day_dir = SOLUTIONS_DIR / f"day{day:02d}"
    src = day_dir / "part1.py"
    dest = day_dir / "part2.py"

    if not src.exists():
        raise SystemExit(f"Source file not found: {src.relative_to(ROOT)}")

    day_dir.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        shutil.copy(src, dest)
        print(f"Bootstrapped {dest.relative_to(ROOT)} from part1.py")

    last_hash = file_hash(src)

    print(
        f"Watching {src.relative_to(ROOT)} -> {dest.relative_to(ROOT)} "
        f"(poll every {interval}s). Press Ctrl+C to stop."
    )
    try:
        while True:
            time.sleep(interval)
            current_hash = file_hash(src)
            if current_hash != last_hash:
                shutil.copy(src, dest)
                last_hash = current_hash
                print(f"Synced changes to {dest.relative_to(ROOT)}")
    except KeyboardInterrupt:
        print("Stopped syncing.")


def main() -> None:
    args = parse_args()

    if args.command == "fetch":
        cookie = get_cookie(args.cookie)
        fetch_input(day=args.day, year=args.year, cookie=cookie)
        bootstrap_solution_file(day=args.day, year=args.year)
    elif args.command == "execute":
        run_solution(day=args.day, part=args.part, run_tests=args.test)
    elif args.command == "copy-part":
        copy_part_one_to_two(day=args.day, force=args.force)
    elif args.command == "sync-part2":
        sync_part_two(day=args.day, interval=args.interval)
    else:
        raise SystemExit("Unknown command.")


if __name__ == "__main__":
    main()
