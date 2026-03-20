#!/usr/bin/env python3
"""arXiv RO-CV daily digest pipeline.

Usage (from the project root):
    python src/main.py fetch
    python src/main.py analyze
    python src/main.py build
    python src/main.py all
"""

import sys
import json
import logging
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config
from arxiv_fetcher import fetch_papers
from filter import load_papers, save_summaries, get_summaries as load_summaries
from digest_writer import write_digest

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("arxiv-ro-cv-digest")


# ------------------------------------------------------------------
# fetch
# ------------------------------------------------------------------


def cmd_fetch(_args):
    """Fetch today's papers from arXiv RSS + API and write data/papers.json."""
    config.ensure_dirs()

    papers = fetch_papers(config.CATEGORIES)

    output = config.DATA_DIR / "papers.json"
    with open(output, "w", encoding="utf-8") as fh:
        json.dump(papers, fh, indent=2, ensure_ascii=False)

    logger.info("Wrote %d papers to %s", len(papers), output)

    type_counts: dict = {}
    for p in papers:
        t = p.get("announce_type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

    print(f"\n{'=' * 60}")
    print(f"Fetched {len(papers)} papers (new + cross) from arXiv")
    print(f"Categories: {', '.join(config.CATEGORIES)}")
    for t, c in sorted(type_counts.items()):
        print(f"  {t}: {c}")
    print(f"Output: {output}")
    print(f"{'=' * 60}")


# ------------------------------------------------------------------
# analyze (filter + summarize + classify via LLM subagent)
# ------------------------------------------------------------------


def cmd_analyze(_args):
    """Prepare for LLM analysis (filter + summarize + classify)."""
    config.ensure_dirs()
    papers = load_papers()
    save_summaries(papers)
    print(f"\n{'=' * 60}")
    print(f"Loaded {len(papers)} papers from data/papers.json")
    print("Use LLM subagents to analyze papers -> data/summaries.json")
    print("After analysis, run: python src/main.py build")
    print(f"{'=' * 60}")


# ------------------------------------------------------------------
# build (generate markdown digest)
# ------------------------------------------------------------------


def cmd_build(_args):
    """Generate markdown digest from summaries."""
    config.ensure_dirs()
    summaries = load_summaries()
    digest_path = write_digest(summaries)
    print(f"\n{'=' * 60}")
    print(f"Generated digest: {digest_path}")
    print(f"{'=' * 60}")


# ------------------------------------------------------------------
# all (full pipeline)
# ------------------------------------------------------------------


def cmd_all(_args):
    """Run fetch + analyze + build."""
    config.ensure_dirs()

    print("\n=== Step 1: Fetch ===")
    papers = fetch_papers(config.CATEGORIES)
    output = config.DATA_DIR / "papers.json"
    with open(output, "w", encoding="utf-8") as fh:
        json.dump(papers, fh, indent=2, ensure_ascii=False)
    print(f"Fetched {len(papers)} papers")

    print("\n=== Step 2: Analyze ===")
    print("Use LLM subagents to analyze papers -> data/summaries.json")
    print("After analysis, run: python src/main.py build")

    print("\n=== Step 3: Build ===")
    print("Run: python src/main.py build")


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="arXiv RO-CV daily digest pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("fetch", help="Fetch today's papers from arXiv")

    sub.add_parser("analyze", help="Prepare for LLM analysis (filter + summarize)")

    sub.add_parser("build", help="Generate markdown digest from summaries")

    sub.add_parser("all", help="Run full pipeline (fetch + analyze + build)")

    args = parser.parse_args()

    if args.command == "fetch":
        cmd_fetch(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "build":
        cmd_build(args)
    elif args.command == "all":
        cmd_all(args)


if __name__ == "__main__":
    main()
