"""Medical paper filtering using LLM judgment."""

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


def save_filtered(papers: list):
    """Save filtered (non-medical) papers to data/filtered.json."""
    with open(_FILTERED_FILE, "w", encoding="utf-8") as fh:
        json.dump(papers, fh, indent=2, ensure_ascii=False)
    logger.info("Saved %d non-medical papers to %s", len(papers), _FILTERED_FILE)


def get_filtered_papers() -> list:
    """Load filtered papers from data/filtered.json."""
    with open(_FILTERED_FILE, encoding="utf-8") as fh:
        return json.load(fh)
