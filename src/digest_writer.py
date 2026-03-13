"""Markdown digest writer for arXiv RO-CV papers."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import config


def load_summaries() -> list:
    """Load summaries from data/summaries.json."""
    summaries_path = config.DATA_DIR / "summaries.json"
    with open(summaries_path, encoding="utf-8") as fh:
        return json.load(fh)


def group_by_topic(summaries: list) -> dict:
    """Group papers by topic. A paper can appear under multiple topics."""
    groups = {}
    for s in summaries:
        topics = s.get("topics", [])
        if not topics:
            topics = ["Other"]
        for topic in topics:
            if topic not in groups:
                groups[topic] = []
            groups[topic].append(s)
    return groups


def write_digest(
    summaries: list,
    output_path: Optional[str] = None,
) -> str:
    """Render *summaries* as a structured markdown digest.

    Returns the path the digest was written to.
    """
    date_str = datetime.now().strftime("%Y-%m-%d")

    if output_path is None:
        output_path = str(config.DIGESTS_DIR / f"{date_str}.md")

    groups = group_by_topic(summaries)

    topic_order = [
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
    topic_set = set(topic_order)

    def topic_sort_key(t: str) -> tuple:
        if t in topic_set:
            return (0, topic_order.index(t), t)
        return (1, 0, t)

    sorted_topics = sorted(groups.keys(), key=topic_sort_key)

    total_papers = sum(len(papers) for papers in groups.values())

    lines = [
        f"# arXiv RO-CV Digest — {date_str}",
        "",
        f"**{total_papers} paper(s) found across {len(groups)} topic(s).**",
        "",
    ]

    for topic in sorted_topics:
        papers = groups[topic]
        lines.append(f"## Topic: {topic}")
        lines.append("")

        for i, paper in enumerate(papers, 1):
            lines.append(f"### {i}. {paper['title']}")
            lines.append("")

            arxiv_id = paper.get("arxiv_id", "")
            arxiv_url = paper.get("arxiv_url", f"https://arxiv.org/abs/{arxiv_id}")
            lines.append(f"- **arXiv**: [{arxiv_id}]({arxiv_url})")

            pdf_url = paper.get("pdf_url", f"https://arxiv.org/pdf/{arxiv_id}.pdf")
            lines.append(f"- **PDF**: [Link]({pdf_url})")

            authors = paper.get("authors", [])
            if authors:
                author_str = ", ".join(authors[:3])
                if len(authors) > 3:
                    author_str += " et al."
                lines.append(f"- **Authors**: {author_str}")

            category = paper.get("primary_category", "")
            if category:
                lines.append(f"- **Category**: {category}")

            topics = paper.get("topics", [])
            if topics:
                lines.append(f"- **Topics**: {', '.join(topics)}")

            lines.append("")

            problem = paper.get("problem", "")
            if problem:
                lines.append(f"**Problem**: {problem}")
                lines.append("")

            innovations = paper.get("innovations", "")
            if innovations:
                lines.append(f"**Innovations**: {innovations}")
                lines.append("")

            keywords = paper.get("keywords", [])
            if keywords:
                lines.append(f"**Keywords**: {', '.join(keywords)}")
                lines.append("")

            lines.append("---")
            lines.append("")

    content = "\n".join(lines)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(content, encoding="utf-8")
    return output_path
