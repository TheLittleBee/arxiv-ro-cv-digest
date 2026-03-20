"""Paper filtering utilities (medical, satellite, 360, event camera)."""

import json
import logging
from pathlib import Path

import config

logger = logging.getLogger(__name__)

_FILTERED_FILE = config.DATA_DIR / "filtered.json"


def load_papers() -> list:
    """Load papers from data/papers.json."""
    papers_path = config.DATA_DIR / "papers.json"
    with open(papers_path, encoding="utf-8") as fh:
        return json.load(fh)


def save_summaries(summaries: list):
    """Save analyzed papers to data/summaries.json."""
    summaries_path = config.DATA_DIR / "summaries.json"
    with open(summaries_path, "w", encoding="utf-8") as fh:
        json.dump(summaries, fh, indent=2, ensure_ascii=False)
    logger.info("Saved %d papers to %s", len(summaries), summaries_path)


def get_summaries() -> list:
    """Load summaries from data/summaries.json."""
    summaries_path = config.DATA_DIR / "summaries.json"
    with open(summaries_path, encoding="utf-8") as fh:
        return json.load(fh)
