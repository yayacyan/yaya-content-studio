# Contributing

Thanks for taking a look at `yaya-content-studio`.

This project is still small on purpose. The goal is to keep it useful for individual creators who want a local, calm, transparent content workflow.

## What kind of contributions fit

- Small CLI improvements
- Clearer docs and examples
- Better rule-based analysis
- Better Markdown templates
- Safer local file handling
- Tests for command behavior

## What does not fit v1

- Auto-publishing to platforms
- Required external APIs
- Required cloud storage
- Tracking private creator data in the repository
- Generic AI-generated writing that removes personal context

## Before opening a pull request

Please check:

- The app still works without third-party dependencies unless the change clearly needs one.
- Sample CSV data is fictional and safe to publish.
- No API keys, tokens, private URLs, personal drafts, or real analytics are committed.
- New behavior is documented in `README.md` or `docs/`.

## Local check

Run the basic commands from the project root:

```bash
python main.py list
python main.py analyze
python main.py suggest
```

If your machine uses `python3`:

```bash
python3 main.py list
python3 main.py analyze
python3 main.py suggest
```

For interactive commands, try them with fictional data:

```bash
python main.py new
python main.py save
python main.py stats
```

## Style

Keep the tone natural and practical. This is a tool for personal creators, not a corporate content platform.
