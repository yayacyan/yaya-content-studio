import argparse
import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main


class CliWorkflowTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)
        self.original_paths = {
            "BASE_DIR": main.BASE_DIR,
            "DATA_DIR": main.DATA_DIR,
            "ARTICLES_DIR": main.ARTICLES_DIR,
            "IDEAS_FILE": main.IDEAS_FILE,
            "STATS_FILE": main.STATS_FILE,
        }
        main.BASE_DIR = self.base_dir
        main.DATA_DIR = self.base_dir / "data"
        main.ARTICLES_DIR = self.base_dir / "articles"
        main.IDEAS_FILE = main.DATA_DIR / "content_ideas.csv"
        main.STATS_FILE = main.DATA_DIR / "stats.csv"
        main.ensure_files()

    def tearDown(self):
        for name, value in self.original_paths.items():
            setattr(main, name, value)
        self.temp_dir.cleanup()

    def read_rows(self, path):
        with path.open(newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def test_new_adds_idea_row(self):
        answers = [
            "note",
            "How I organize content ideas after work",
            "workflow",
            "independent creators with a day job",
            "no",
            "Sample memo",
        ]

        with patch("builtins.input", side_effect=answers), redirect_stdout(io.StringIO()):
            main.command_new(argparse.Namespace())

        rows = self.read_rows(main.IDEAS_FILE)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], "1")
        self.assertEqual(rows[0]["platform"], "note")
        self.assertEqual(rows[0]["status"], "idea")
        self.assertEqual(rows[0]["paid"], "no")

    def test_save_writes_markdown_with_front_matter(self):
        answers = [
            "Draft title",
            "Medium",
            "workflow",
            "Open Source, Python, Creator Tools",
            "# Draft title",
            "",
            "Body paragraph.",
            ".",
        ]

        with patch("builtins.input", side_effect=answers), redirect_stdout(io.StringIO()):
            main.command_save(argparse.Namespace())

        article_files = list(main.ARTICLES_DIR.glob("**/*.md"))
        self.assertEqual(len(article_files), 1)
        content = article_files[0].read_text(encoding="utf-8")
        self.assertIn("title: Draft title", content)
        self.assertIn("platform: Medium", content)
        self.assertIn("category: workflow", content)
        self.assertIn("tags: Open Source, Python, Creator Tools", content)
        self.assertIn("status: draft", content)
        self.assertIn("Body paragraph.", content)

    def test_analyze_and_suggest_use_stats_signals(self):
        main.append_csv(
            main.IDEAS_FILE,
            main.IDEA_FIELDS,
            {
                "id": "1",
                "date": "2026-01-10",
                "platform": "note",
                "title": "A separate recent idea",
                "category": "workflow",
                "target_reader": "creators",
                "paid": "no",
                "status": "idea",
                "memo": "Sample",
            },
        )
        main.append_csv(
            main.STATS_FILE,
            main.STATS_FIELDS,
            {
                "date": "2026-01-15",
                "platform": "note",
                "title": "How I organize content ideas after work",
                "category": "workflow",
                "views": "800",
                "likes": "32",
                "comments": "4",
                "claps": "0",
                "sales": "0",
                "memo": "Sample data only",
            },
        )

        analyze_output = io.StringIO()
        with redirect_stdout(analyze_output):
            main.command_analyze(argparse.Namespace())

        self.assertIn("Best platform: note", analyze_output.getvalue())
        self.assertIn("Good paid article candidates", analyze_output.getvalue())

        suggest_output = io.StringIO()
        with redirect_stdout(suggest_output):
            main.command_suggest(argparse.Namespace())

        self.assertIn("Next topic suggestions", suggest_output.getvalue())
        self.assertIn("付費版", suggest_output.getvalue())


if __name__ == "__main__":
    unittest.main()
