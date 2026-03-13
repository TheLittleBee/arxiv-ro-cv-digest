---
name: arxiv-ro-cv-digest
description: >
  Fetch daily arXiv announcements (cs.RO, cs.CV), filter medical papers,
  generate structured markdown digest with topic classification, problem
  summaries, innovations, and keywords. Use when: (1) User wants daily arXiv
  robotics/CV paper digest, (2) Summarizing papers from cs.RO/cs.CV categories,
  (3) Filtering medical/clinical papers, (4) Classifying papers by topic (VLM,
  VLA, Gaussian Splatting, etc.)
---

# arXiv RO-CV Daily Digest

All paths below are relative to this skill's root directory.

## Quick reference

| Item | Value |
|------|-------|
| **Categories** | `cs.RO`, `cs.CV` |
| **Announce types** | `new` and `cross` only |
| **Digest output** | `digests/YYYY-MM-DD.md` |
| **Intermediate data** | `data/papers.json`, `data/filtered.json`, `data/summaries.json` |

---

## Invocation protocol

This is a **four-step** skill. Execute the steps in order.
All shell commands assume the working directory is the skill root.

### Step 1 — Fetch papers

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py fetch
```

Fetches the arXiv RSS Atom feed for `cs.RO` and `cs.CV`, enriches each paper
with metadata from the arXiv Search API, filters to `new` and `cross`
announcements, and writes the result to `data/papers.json`.

### Step 2 — Filter medical papers

Read `data/papers.json`. For **every** paper, judge whether it is
medical/clinical focused based on its **title and abstract**. Write the
verdicts to `data/filtered.json`.

**You MUST use LLM subagents to perform this judgment.** Do NOT apply
keyword matching or heuristics. Every paper must be evaluated by an LLM.

To avoid timeouts, split the papers into batches of **≤ 30 papers**
and process batches in parallel via subagents. Each subagent receives a
batch and returns a JSON array of verdicts.

#### Output format for `data/filtered.json`

```json
[
  {
    "arxiv_id": "2603.01234",
    "is_medical": false,
    "reason": "One-sentence explanation"
  },
  {
    "arxiv_id": "2603.01235",
    "is_medical": true,
    "reason": "Focuses on medical imaging analysis for tumor detection"
  }
]
```

The file must contain an entry for **every** paper in `data/papers.json`.

#### Medical paper criteria

A paper is medical if it focuses on:
- Medical imaging (CT, MRI, X-ray, ultrasound for diagnosis)
- Clinical applications, disease diagnosis, treatment planning
- Drug discovery, pharmaceutical research, genomic analysis
- Biomedical devices, prosthetics, neural implants
- Patient monitoring, healthcare systems

A paper is NOT medical if it:
- Uses computer vision/robotics for general-purpose tasks
- Applies ML to images without clinical context
- Discusses sensor hardware without medical application

### Step 3 — Summarize and classify

Read `data/filtered.json`. For **every non-medical paper**, generate a summary
including: problem solved, main innovations (2-3 key contributions),
keywords (3-5), and topic classification. Write to `data/summaries.json`.

**You MUST use LLM subagents to perform summarization.**

#### Output format for `data/summaries.json`

```json
[
  {
    "arxiv_id": "2603.01234",
    "title": "Paper Title",
    "arxiv_url": "https://arxiv.org/abs/2603.01234",
    "pdf_url": "https://arxiv.org/pdf/2603.01234.pdf",
    "authors": ["Author 1", "Author 2"],
    "primary_category": "cs.RO",
    "problem": "What problem this paper solves",
    "innovations": "Key innovation 1. Key innovation 2. Key innovation 3.",
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "topics": ["VLM (Vision-Language Models)", "Embodied AI"]
  }
]
```

#### Topic classification

Assign **one or more** topics from this list. If no topic fits, create a new one:
- **VLM (Vision-Language Models)**: Vision-language models, multimodal LLMs
- **VLA (Vision-Language-Action)**: Robot policies, embodied AI agents
- **Gaussian Splatting**: 3DGS, novel view synthesis, radiance fields
- **Spatial Intelligence**: Scene understanding, 3D perception, affordances
- **Manipulation**: Robot grasping, Dexterous manipulation, Assembly
- **Autonomous Driving**: Self-driving, vehicle navigation, traffic
- **3D Reconstruction**: Structure from motion, depth estimation, SLAM
- **Video Understanding**: Action recognition, video captioning, temporal modeling
- **Embodied AI**: Agents in simulation, virtual environments, humanoids
- **Navigation**: Path planning, exploration, localization
- **Other**: Does not fit above categories

### Step 4 — Generate digest

```bash
python src/main.py build
```

Reads `data/summaries.json` and writes a structured markdown digest to
`digests/YYYY-MM-DD.md`, grouped by topic.

After this step, **present the contents of `digests/YYYY-MM-DD.md`** to
the user as the daily report.

---

## Scheduling notes

- The arXiv RSS feed updates **daily around midnight US Eastern Time**
  (~13:00 GMT+8 during EST, ~12:00 GMT+8 during EDT).
- **No updates on Saturday or Sunday.** Monday's feed contains Friday's
  submissions. This skill should not be invoked on weekends.
- Invoke this skill once daily, after the RSS feed has updated.

---

## Setup

A Python virtual environment is used to isolate dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/web/simple
```

If the venv already exists, just activate it before running commands:

```bash
source .venv/bin/activate
```

---

## Attribution

Thank you to arXiv for use of its open access interoperability.
