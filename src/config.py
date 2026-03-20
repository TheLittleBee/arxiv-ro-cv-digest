"""Project configuration and environment loading."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DIGESTS_DIR = PROJECT_ROOT / "digests"

CATEGORIES = ["cs.RO", "cs.CV"]

ARXIV_RSS_BASE = "https://rss.arxiv.org/atom"
ARXIV_API_BASE = "https://export.arxiv.org/api/query"

TOPICS = [
    "Gaussian Splatting",
    "3D Reconstruction",
    "World Model",
    "Spatial Intelligence",
    "Diffusion/Flow Match",
    "VLA/VLM",
    "Manipulation",
    "Robotic",
    "Autonomous",
    "Other",
]


def ensure_dirs():
    """Ensure output directories exist."""
    DATA_DIR.mkdir(exist_ok=True)
    DIGESTS_DIR.mkdir(exist_ok=True)
