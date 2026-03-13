#!/usr/bin/env python3
"""arXiv RO-CV daily digest pipeline.

Usage (from the project root):
    python src/main.py fetch
    python src/main.py filter
    python src/main.py summarize
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
from medical_filter import load_papers, save_filtered, get_filtered_papers
from summarizer import load_filtered_papers, save_summaries, get_summaries
from digest_writer import load_summaries, write_digest

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
# filter
# ------------------------------------------------------------------


def cmd_filter(_args):
    """Load papers and save to filtered.json (filtering done by agent)."""
    config.ensure_dirs()
    papers = load_papers()
    save_filtered(papers)
    print(f"\n{'=' * 60}")
    print(f"Loaded {len(papers)} papers from data/papers.json")
    print("Use LLM subagents to filter medical papers -> data/filtered.json")
    print(f"{'=' * 60}")


# ------------------------------------------------------------------
# summarize
# ------------------------------------------------------------------


def cmd_summarize(_args):
    """Load filtered papers and save summaries (summarization done by agent)."""
    config.ensure_dirs()
    papers = get_filtered_papers()
    save_summaries(papers)
    print(f"\n{'=' * 60}")
    print(f"Loaded {len(papers)} papers from data/filtered.json")
    print("Use LLM subagents to generate summaries -> data/summaries.json")
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
    """Run fetch + filter + summarize + build."""
    config.ensure_dirs()

    print("\n=== Step 1: Fetch ===")
    papers = fetch_papers(config.CATEGORIES)
    output = config.DATA_DIR / "papers.json"
    with open(output, "w", encoding="utf-8") as fh:
        json.dump(papers, fh, indent=2, ensure_ascii=False)
    print(f"Fetched {len(papers)} papers")

    print("\n=== Step 2: Filter ===")
    print("Use LLM subagents to filter medical papers -> data/filtered.json")
    print("Then run: python src/main.py filter-exec")

    print("\n=== Step 3: Summarize ===")
    print("Use LLM subagents to summarize -> data/summaries.json")
    print("Then run: python src/main.py build")


# ------------------------------------------------------------------
# filter-exec (execute filtered data)
# ------------------------------------------------------------------


def cmd_filter_exec(_args):
    """Execute filtering based on data/filtered.json from agent."""
    papers = get_filtered_papers()
    print(f"\n{'=' * 60}")
    print(f"Using {len(papers)} filtered papers")
    print(f"{'=' * 60}")


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="arXiv RO-CV daily digest pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("fetch", help="Fetch today's papers from arXiv")

    sub.add_parser("filter", help="Prepare for filtering (agent step)")

    sub.add_parser("filter-exec", help="Execute with filtered data")

    sub.add_parser("summarize", help="Prepare for summarization (agent step)")

    sub.add_parser("build", help="Generate markdown digest from summaries")

    sub.add_parser("all", help="Run full pipeline (fetch + filter + summarize + build)")

    args = parser.parse_args()

    if args.command == "fetch":
        cmd_fetch(args)
    elif args.command == "filter":
        cmd_filter(args)
    elif args.command == "filter-exec":
        cmd_filter_exec(args)
    elif args.command == "summarize":
        cmd_summarize(args)
    elif args.command == "build":
        cmd_build(args)
    elif args.command == "all":
        cmd_all(args)


if __name__ == "__main__":
    main()
