from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cs_pipeline import run_pipeline  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the deterministic CS triage demo.")
    parser.add_argument("seed", nargs="?", default=Path("tests/fixtures/cs_seed.json"), type=Path)
    parser.add_argument("--output", default=Path("dist/cs_demo_report.md"), type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = run_pipeline(args.seed, args.output)
    print(f"Wrote {len(report.tickets)} analyzed tickets to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
