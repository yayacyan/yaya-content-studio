# yaya-content-studio

Language: [繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md)

`yaya-content-studio` is a local CLI tool for individual content creators.

It is not an article generator, and it does not auto-publish anything. Think of it as a quiet content operations assistant: it helps you collect ideas, save Markdown drafts, record article performance, generate no-cost SVG covers, and decide what to write next with simple local rules.

Version 1 is local-first. It does not call APIs, does not require an account, and does not send your writing to external services. Data is stored as CSV and Markdown inside the project folder.

![yaya-content-studio CLI demo](docs/assets/demo.svg)

## Project Links

- [Usage examples](docs/usage_examples.md)
- [Content strategy notes](docs/content_strategy.md)
- [Launch article draft](docs/launch_article.md)
- [Roadmap](docs/roadmap.md)

## Who This Is For

This tool is for creators who:

- Write on note, Medium, Threads, or X
- Have many ideas but often lose the context behind them
- Want to separate free articles from paid articles
- Want to review topic performance without relying only on memory
- Prefer simple local files like Markdown and CSV
- Do not want to connect APIs or cloud services at the beginning

It works especially well for personal creators, small knowledge workers, and people who want to turn daily experience into publishable content.

## Installation

Check that Python 3 is available:

```bash
python --version
```

If your system does not have `python`, try:

```bash
python3 --version
```

Clone or download the repository, then enter the folder:

```bash
cd yaya-content-studio
```

Version 1 has no third-party dependencies. `requirements.txt` is kept for future versions.

Optional virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If your machine uses `python3`, replace `python` with `python3`.

## Basic Workflow

1. Capture new topics with `new`
2. Save article drafts with `save`
3. Generate no-cost SVG covers with `cover`
4. Manually edit and publish to note, Medium, Threads, or X
5. Record performance with `stats`
6. Review patterns with `analyze`
7. Get next-topic ideas with `suggest`

This tool will not decide your direction for you. It simply keeps the small pieces of content work in one place so the next decision is easier.

## Commands

Run commands from the project root:

```bash
python main.py <command>
```

If your machine uses `python3`:

```bash
python3 main.py <command>
```

### Add a Content Idea

```bash
python main.py new
```

Inputs:

- platform: note / Medium / Threads / X
- title
- category
- target_reader
- paid: yes / no
- memo

Saved to:

```text
data/content_ideas.csv
```

### Save an Article Draft

```bash
python main.py save
```

Inputs:

- title
- platform
- category
- tags
- body markdown

Finish body input with a single `.` line.

Drafts are saved to:

```text
articles/YYYY/MM/YYYYMMDD_platform_title.md
```

Front matter:

```markdown
---
title:
date:
platform:
category:
tags:
status: draft
---
```

### Generate a No-Cost Cover

```bash
python main.py cover
```

Inputs:

- title
- platform
- category
- tags
- subtitle

This command does not call image APIs and does not require paid services. It creates a local SVG cover:

```text
exports/covers/YYYY/MM/YYYYMMDD_platform_title_cover.svg
```

`exports/` is ignored by Git by default, so personal publishing assets stay local.

### List Recent Content

```bash
python main.py list
```

Shows recent content ideas and Markdown drafts.

### Record Article Performance

```bash
python main.py stats
```

Inputs:

- date
- platform
- title
- views
- likes
- comments
- claps
- sales
- memo

Saved to:

```text
data/stats.csv
```

### Analyze Performance

```bash
python main.py analyze
```

Outputs simple rule-based analysis:

- Best-performing platform
- Best-performing category
- Articles with likes but no sales
- Articles that may become paid content
- Next-step suggestions

### Suggest Next Topics

```bash
python main.py suggest
```

Recommends 5 next-topic ideas based on `content_ideas.csv` and `stats.csv`.

Current rules:

- Avoid topics too similar to the latest 5 ideas
- Turn high-like, low-sales topics into more concrete paid article ideas
- Extend categories that perform well
- Output note and Medium title versions

## Example note / Medium Workflow

Suppose you want to write about organizing content ideas after working abroad.

1. Save the idea with `python main.py new`
2. Draft a more personal note article with `python main.py save`
3. Generate a free SVG cover with `python main.py cover`
4. If it performs well, turn the topic into a more structured Medium article
5. Record views, likes, comments, and sales with `python main.py stats`
6. Run `python main.py analyze` and `python main.py suggest`

Free articles are mostly for resonance and trust. Paid articles should solve a concrete problem and include process, mistakes, templates, and real examples.

## Roadmap

### v1: Local CLI

- Add content ideas
- Save Markdown drafts
- Generate no-cost SVG covers
- List recent ideas and drafts
- Record article performance
- Analyze simple signals
- Suggest next topics

### v2: Better Local Workflow

- Search and filter ideas
- Update article status
- Generate weekly reviews
- Add richer paid article templates
- Export draft bundles
- Add more cover styles and optional PNG export

### v3: Optional Integrations

- Optional AI-assisted summaries or reviews
- Optional platform data import
- Optional content calendar

Auto-publishing is intentionally not an early goal. For personal creators, stabilizing the writing workflow matters more than connecting every tool at once.
