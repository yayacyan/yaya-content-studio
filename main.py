from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ARTICLES_DIR = BASE_DIR / "articles"
IDEAS_FILE = DATA_DIR / "content_ideas.csv"
STATS_FILE = DATA_DIR / "stats.csv"

IDEA_FIELDS = [
    "id",
    "date",
    "platform",
    "title",
    "category",
    "target_reader",
    "paid",
    "status",
    "memo",
]

STATS_FIELDS = [
    "date",
    "platform",
    "title",
    "category",
    "views",
    "likes",
    "comments",
    "claps",
    "sales",
    "memo",
]

VALID_PLATFORMS = {"note", "Medium", "Threads", "X"}


def ensure_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    ensure_csv(IDEAS_FILE, IDEA_FIELDS)
    ensure_csv(STATS_FILE, STATS_FIELDS)


def ensure_csv(path: Path, fields: list[str]) -> None:
    if path.exists():
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()


def read_csv(path: Path) -> list[dict[str, str]]:
    ensure_files()
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def append_csv(path: Path, fields: list[str], row: dict[str, str]) -> None:
    ensure_files()
    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writerow({field: row.get(field, "") for field in fields})


def prompt_required(label: str) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print(f"{label} is required.")


def prompt_choice(label: str, choices: set[str]) -> str:
    normalized = {choice.lower(): choice for choice in choices}
    while True:
        value = prompt_required(label)
        match = normalized.get(value.lower())
        if match:
            return match
        print(f"Please enter one of: {', '.join(sorted(choices))}")


def prompt_number(label: str) -> str:
    while True:
        value = input(f"{label}: ").strip() or "0"
        try:
            number = int(value)
        except ValueError:
            print(f"{label} must be a number.")
            continue
        if number < 0:
            print(f"{label} must be 0 or greater.")
            continue
        return str(number)


def prompt_markdown_body() -> str:
    print("body markdown: enter your draft. Finish with a single '.' line.")
    lines: list[str] = []
    while True:
        line = input()
        if line == ".":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def next_id(rows: list[dict[str, str]]) -> str:
    ids = []
    for row in rows:
        try:
            ids.append(int(row.get("id", "0")))
        except ValueError:
            continue
    return str(max(ids, default=0) + 1)


def slugify(value: str) -> str:
    slug = re.sub(r"[^\w\u4e00-\u9fff\u3040-\u30ff]+", "-", value.strip(), flags=re.UNICODE)
    slug = re.sub(r"-+", "-", slug).strip("-_")
    return slug or "untitled"


def command_new(_: argparse.Namespace) -> None:
    rows = read_csv(IDEAS_FILE)
    row = {
        "id": next_id(rows),
        "date": date.today().isoformat(),
        "platform": prompt_choice("platform (note / Medium / Threads / X)", VALID_PLATFORMS),
        "title": prompt_required("title"),
        "category": prompt_required("category"),
        "target_reader": prompt_required("target_reader"),
        "paid": prompt_choice("paid (yes / no)", {"yes", "no"}),
        "status": "idea",
        "memo": input("memo: ").strip(),
    }
    append_csv(IDEAS_FILE, IDEA_FIELDS, row)
    print(f"Added idea #{row['id']}: {row['title']}")


def command_save(_: argparse.Namespace) -> None:
    title = prompt_required("title")
    platform = prompt_choice("platform (note / Medium / Threads / X)", VALID_PLATFORMS)
    category = prompt_required("category")
    body = prompt_markdown_body()

    today = date.today()
    article_dir = ARTICLES_DIR / today.strftime("%Y") / today.strftime("%m")
    article_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"{today.strftime('%Y%m%d')}_{slugify(platform)}_{slugify(title)}.md"
    path = article_dir / file_name

    content = "\n".join(
        [
            "---",
            f"title: {title}",
            f"date: {today.isoformat()}",
            f"platform: {platform}",
            f"category: {category}",
            "status: draft",
            "---",
            "",
            body,
            "",
        ]
    )
    path.write_text(content, encoding="utf-8")
    print(f"Saved article: {path.relative_to(BASE_DIR)}")


def command_list(_: argparse.Namespace) -> None:
    ideas = read_csv(IDEAS_FILE)
    print("Recent content ideas")
    print("--------------------")
    if ideas:
        for row in ideas[-20:][::-1]:
            print(
                f"#{row.get('id')} {row.get('date')} [{row.get('platform')}] "
                f"{row.get('title')} ({row.get('category')}, {row.get('status')})"
            )
    else:
        print("No content ideas yet.")

    print("\nRecent articles")
    print("---------------")
    article_files = sorted(ARTICLES_DIR.glob("**/*.md"), key=lambda path: path.stat().st_mtime, reverse=True)
    if article_files:
        for path in article_files[:20]:
            print(path.relative_to(BASE_DIR))
    else:
        print("No articles yet.")


def command_stats(_: argparse.Namespace) -> None:
    row = {
        "date": prompt_required("date (YYYY-MM-DD)"),
        "platform": prompt_choice("platform (note / Medium / Threads / X)", VALID_PLATFORMS),
        "title": prompt_required("title"),
        "category": prompt_required("category"),
        "views": prompt_number("views"),
        "likes": prompt_number("likes"),
        "comments": prompt_number("comments"),
        "claps": prompt_number("claps"),
        "sales": prompt_number("sales"),
        "memo": input("memo: ").strip(),
    }
    append_csv(STATS_FILE, STATS_FIELDS, row)
    print(f"Recorded stats: {row['title']}")


def as_int(row: dict[str, str], key: str) -> int:
    try:
        return int(row.get(key, "0") or "0")
    except ValueError:
        return 0


def engagement_score(row: dict[str, str]) -> int:
    return as_int(row, "likes") + as_int(row, "comments") * 2 + as_int(row, "claps")


def grouped_scores(rows: list[dict[str, str]], key: str) -> dict[str, int]:
    scores: dict[str, int] = defaultdict(int)
    for row in rows:
        name = row.get(key, "").strip() or "uncategorized"
        scores[name] += engagement_score(row) + as_int(row, "sales") * 5
    return dict(scores)


def best_group(rows: list[dict[str, str]], key: str) -> tuple[str, int] | None:
    scores = grouped_scores(rows, key)
    if not scores:
        return None
    return max(scores.items(), key=lambda item: item[1])


def command_analyze(_: argparse.Namespace) -> None:
    rows = read_csv(STATS_FILE)
    if not rows:
        print("No stats yet. Run `python main.py stats` first.")
        return

    best_platform = best_group(rows, "platform")
    best_category = best_group(rows, "category")
    likes_no_sales = [row for row in rows if as_int(row, "likes") > 0 and as_int(row, "sales") == 0]
    paid_candidates = [
        row
        for row in rows
        if engagement_score(row) >= 10 and as_int(row, "sales") == 0
    ]

    print("Performance analysis")
    print("--------------------")
    if best_platform:
        print(f"Best platform: {best_platform[0]} (score {best_platform[1]})")
    if best_category:
        print(f"Best category: {best_category[0]} (score {best_category[1]})")

    print("\nArticles with likes but no sales")
    if likes_no_sales:
        for row in likes_no_sales:
            print(f"- {row.get('title')} [{row.get('platform')}] likes={row.get('likes')}")
    else:
        print("- None")

    print("\nGood paid article candidates")
    if paid_candidates:
        for row in paid_candidates:
            print(f"- {row.get('title')} ({row.get('category')})")
    else:
        print("- None yet. Look for posts with repeated likes/comments but low sales.")

    print("\nNext step suggestions")
    if best_category:
        print(f"- Create a small series around `{best_category[0]}`.")
    if likes_no_sales:
        print("- Turn high-like, no-sale topics into concrete problem-solving paid drafts.")
    print("- For each paid draft, include process, mistakes, templates, and real examples.")


def normalize_title(title: str) -> set[str]:
    words = re.findall(r"[\w\u4e00-\u9fff\u3040-\u30ff]+", title.lower(), flags=re.UNICODE)
    return {word for word in words if len(word) > 1}


def too_similar(title: str, recent_titles: list[str]) -> bool:
    current = normalize_title(title)
    if not current:
        return False
    for recent in recent_titles:
        other = normalize_title(recent)
        overlap = len(current & other) / max(len(current), 1)
        if overlap >= 0.6:
            return True
    return False


def make_suggestion(base_title: str, category: str, reason: str) -> dict[str, str]:
    topic = f"{base_title}：流程、失敗與實際例子"
    return {
        "topic": topic,
        "category": category or "未分類",
        "reason": reason,
        "note": f"{topic}｜我在日本工作後的真實整理",
        "Medium": f"How I Think About {base_title}: Process, Mistakes, and Practical Examples",
    }


def command_suggest(_: argparse.Namespace) -> None:
    ideas = read_csv(IDEAS_FILE)
    stats = read_csv(STATS_FILE)
    recent_titles = [row.get("title", "") for row in ideas[-5:]]
    suggestions: list[dict[str, str]] = []

    for row in sorted(stats, key=engagement_score, reverse=True):
        title = row.get("title", "").strip()
        if not title or too_similar(title, recent_titles):
            continue
        if as_int(row, "likes") > 0 and as_int(row, "sales") == 0:
            suggestions.append(
                make_suggestion(
                    f"{title}的付費版",
                    row.get("category", ""),
                    "likes 多但 sales 少，適合改成更具體的付費題材。",
                )
            )
        if len(suggestions) >= 5:
            break

    best_category = best_group(stats, "category")
    if best_category:
        category = best_category[0]
        series_titles = [
            f"{category}入門時最容易卡住的 3 件事",
            f"{category}的實際流程整理",
            f"{category}失敗案例與修正方式",
        ]
        for title in series_titles:
            if len(suggestions) >= 5:
                break
            if not too_similar(title, recent_titles):
                suggestions.append(make_suggestion(title, category, "這個 category 反應好，適合延伸系列文。"))

    for row in ideas:
        title = row.get("title", "").strip()
        if len(suggestions) >= 5:
            break
        if title and not too_similar(title, recent_titles):
            suggestions.append(make_suggestion(title, row.get("category", ""), "從既有 idea 延伸，但避開最近 5 篇相似主題。"))

    fallback_titles = [
        ("在日本工作後，我重新整理內容創作節奏", "content"),
        ("免費文和付費文到底要差在哪裡", "monetization"),
        ("把 Threads 靈感整理成 note 長文的方法", "workflow"),
        ("一篇文章從生活經驗變成可販售內容的流程", "paid content"),
        ("寫不出來時如何用舊文章找到下一題", "workflow"),
    ]
    for title, category in fallback_titles:
        if len(suggestions) >= 5:
            break
        if not too_similar(title, recent_titles):
            suggestions.append(make_suggestion(title, category, "資料還不多，先用符合定位的基礎題材補足內容池。"))

    print("Next topic suggestions")
    print("----------------------")
    for index, item in enumerate(suggestions[:5], start=1):
        print(f"{index}. Topic: {item['topic']}")
        print(f"   Category: {item['category']}")
        print(f"   Reason: {item['reason']}")
        print(f"   note: {item['note']}")
        print(f"   Medium: {item['Medium']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local content operations assistant.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    commands = {
        "new": command_new,
        "save": command_save,
        "list": command_list,
        "stats": command_stats,
        "analyze": command_analyze,
        "suggest": command_suggest,
    }
    for name, handler in commands.items():
        subparser = subparsers.add_parser(name)
        subparser.set_defaults(func=handler)

    return parser


def main() -> None:
    ensure_files()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
