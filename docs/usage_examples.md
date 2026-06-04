# Usage Examples

This page shows a few simple examples using fictional sample data.

## Add a content idea

```bash
python main.py new
```

Example input:

```text
platform: note
title: How I organize content ideas after work
category: workflow
target_reader: independent creators with a day job
paid: no
memo: Free article focused on resonance and routine
```

This adds a row to `data/content_ideas.csv`.

## Save a Markdown draft

```bash
python main.py save
```

Example input:

```text
title: How I organize content ideas after work
platform: note
category: workflow
tags: Creator Tools, Markdown, Local First
body markdown:
# How I organize content ideas after work

I used to keep ideas in too many places. The real problem was not tools, but missing context.

## What changed

Now I save the reader, platform, and reason together.
.
```

The final `.` line ends body input.

The draft is saved under:

```text
articles/YYYY/MM/YYYYMMDD_platform_title.md
```

## Generate a no-cost SVG cover

```bash
python main.py cover
```

Example input:

```text
title: How I organize content ideas after work
platform: note
category: workflow
tags: Creator Tools, Markdown, Local First
subtitle: A local-first workflow for personal creators
```

This saves a local SVG cover under:

```text
exports/covers/YYYY/MM/YYYYMMDD_platform_title_cover.svg
```

The cover command does not call image APIs and does not require paid services.

## Record performance stats

```bash
python main.py stats
```

Example input:

```text
date: 2026-01-15
platform: note
title: How I organize content ideas after work
category: workflow
views: 800
likes: 32
comments: 4
claps: 0
sales: 0
memo: Good resonance, no paid conversion yet
```

This adds a row to `data/stats.csv`.

## Review and choose the next topic

```bash
python main.py analyze
python main.py suggest
```

If an article has likes but no sales, the tool may suggest turning it into a more concrete paid article with process, mistakes, templates, and examples.
