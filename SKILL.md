---
name: arxiv-ro-cv-digest
description: >
  Fetch daily arXiv announcements (cs.RO, cs.CV), filter irrelevant papers
  (medical, satellite remote sensing, 360 panorama, event camera), generate
  structured markdown digest with topic classification, problem summaries, and
  innovations. Use when: (1) User wants daily arXiv robotics/CV paper digest,
  (2) Summarizing papers from cs.RO/cs.CV categories, (3) Filtering papers by
  topic (Gaussian Splatting, World Model, VLA, etc.), (4) Generating daily
  research digests
---

# arXiv RO-CV Daily Digest

All paths below are relative to this skill's root directory.

## Quick reference

| Item | Value |
|------|-------|
| **Categories** | `cs.RO`, `cs.CV` |
| **Announce types** | `new` and `cross` only |
| **Digest output** | `digests/YYYY-MM-DD.md` |
| **Data files** | `data/papers.json`, `data/summaries.json` |
| **Prompt file** | `references/analyze_papers_prompt.md` |

---

## Invocation protocol

This is a **three-step** skill. Execute the steps in order.
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

### Step 2 — Analyze papers (filter + summarize + classify)

Read `data/papers.json`. For **every** paper, use LLM subagents to:
1. Judge whether it should be filtered
2. If not filtered, classify into ONE topic and generate summary

**You MUST use LLM subagent sessions for this analysis.**
Do NOT apply keyword matching, regex rules, or direct LLM API calls.

#### Batch processing

Split papers into batches of **≤ 30 papers**. Process batches in parallel
via subagents. Each subagent receives a batch and returns a JSON array.

#### Subagent prompt

Load the subagent prompt from `references/analyze_papers_prompt.md`.
Use the content of that file as the prompt when invoking subagents for paper analysis.

**Important**: The `problem` and `innovations` fields in the output **must be written in Chinese**.

#### Output file: `data/summaries.json`

Merge all batch results into a single JSON array and save to `data/summaries.json`.

### Step 3 — Generate digest

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
