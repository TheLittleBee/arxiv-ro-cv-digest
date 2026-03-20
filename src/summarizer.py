"""Paper summarization utilities."""

import json
import logging
from pathlib import Path

import config

logger = logging.getLogger(__name__)

_SUMMARIES_FILE = config.DATA_DIR / "summaries.json"


def load_summaries() -> list:
    """Load summaries from data/summaries.json."""
    with open(_SUMMARIES_FILE, encoding="utf-8") as fh:
        return json.load(fh)


def save_summaries(summaries: list):
    """Save summaries to data/summaries.json."""
    with open(_SUMMARIES_FILE, "w", encoding="utf-8") as fh:
        json.dump(summaries, fh, indent=2, ensure_ascii=False)
    logger.info("Saved %d summaries to %s", len(summaries), _SUMMARIES_FILE)
