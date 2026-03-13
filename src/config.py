"""Project configuration and environment loading."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DIGESTS_DIR = PROJECT_ROOT / "digests"

CATEGORIES = ["cs.RO", "cs.CV"]

ARXIV_RSS_BASE = "https://rss.arxiv.org/atom"
ARXIV_API_BASE = "https://export.arxiv.org/api/query"

TOPICS = [
    "VLM (Vision-Language Models)",
    "VLA (Vision-Language-Action)",
    "Gaussian Splatting",
    "Spatial Intelligence",
    "Manipulation",
    "Autonomous Driving",
    "3D Reconstruction",
    "Video Understanding",
    "Embodied AI",
    "Navigation",
    "Other",
]

MEDICAL_KEYWORDS = [
    "medical",
    "medicine",
    "clinical",
    "diagnosis",
    "treatment",
    "patient",
    "disease",
    "pathology",
    "radiology",
    "ct scan",
    "mri",
    "x-ray",
    "ultrasound",
    "biomedical",
    "healthcare",
    "therapeutic",
    "surgery",
    "drug",
    "pharmaceutical",
    "genomic",
    "protein",
    "molecule",
    "drug discovery",
    "medical imaging",
    "neuroradiology",
    "cardiology",
    "oncology",
    "dermatology",
    "ophthalmology",
    "dentistry",
    "veterinary",
    "prosthetic",
    "brain-computer",
    "neural implant",
    "biometric",
    "biosensor",
]


def ensure_dirs():
    """Ensure output directories exist."""
    DATA_DIR.mkdir(exist_ok=True)
    DIGESTS_DIR.mkdir(exist_ok=True)
