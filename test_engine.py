import json
import subprocess
import sys
import unittest
from pathlib import Path

from engine import evaluate


def example():
    return json.loads(Path(__file__).with_name("example.json").read_text(encoding="utf-8"))


class AcceptanceTests(unittest.TestCase):
    def test_example_cli(self):
        proc = subprocess.run([sys.executable, "cli.py", "example.json"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), evaluate(example()))

    def test_gain_regression_and_no_match(self):
        rows = evaluate(example())["queries"]
        self.assertEqual([r["delta"] for r in rows], [1, -1, 0, 0])
        self.assertEqual(rows[-1]["bm25"]["ids"], [])

    def test_partial_recall_denominator(self):
        data = example()
        data["queries"] = [{"id": "both", "text": "retry", "relevant": ["a", "b"]}]
        self.assertEqual(evaluate(data)["macro_recall"], {"bm25": 0.5, "overlap": 0.5})

    def test_unknown_label_rejected(self):
        data = example()
        data["queries"][0]["relevant"] = ["absent"]
        with self.assertRaises(ValueError):
            evaluate(data)
