# yaya-content-studio: a small local CLI for content creators

I built `yaya-content-studio` because my content workflow kept splitting into too many places.

Ideas were in notes, article drafts were in Markdown files, platform stats were somewhere else, and the decision about what to write next was mostly based on memory. That works for a while, but it gets fragile once you write across note, Medium, Threads, and X.

This project is a small attempt to make that workflow calmer.

## What it does

`yaya-content-studio` is a local CLI tool for individual creators.

It helps you:

- Save content ideas
- Save Markdown article drafts
- Record article performance
- See which platforms and categories are working
- Get simple next-topic suggestions

It does not generate articles for you. It does not auto-publish. It does not call external APIs in the first version.

Everything stays local as CSV and Markdown.

## Why local first

For personal creators, not every workflow needs to start with a SaaS dashboard.

Sometimes the better first step is:

- A folder you can understand
- A CSV file you can open
- A Markdown draft you can edit anywhere
- A CLI command that does one small job

Local files make the project less magical, but that is the point. You can inspect the data, move it, back it up, or change the tool later.

## Free content and paid content need different shapes

One thing this tool is designed around is the difference between free and paid content.

Free articles are often for resonance and trust. They should help readers feel seen.

Paid articles should solve a more concrete problem. They need process, mistakes, templates, and real examples.

The current version uses simple rules to notice patterns like:

- This topic gets likes but no sales
- This category keeps performing well
- This platform has better engagement

Those signals are not perfect. But they are usually better than guessing from memory.

## What I want to improve next

The project is early, but the direction is clear:

- Add tests around the CLI workflow
- Improve local search and filtering
- Add better article templates
- Add weekly review reports
- Keep API integrations optional

I want this to stay useful for creators who prefer a transparent, local-first workflow instead of giving every draft and metric to another platform.

Project repo:

https://github.com/yayacyan/yaya-content-studio
