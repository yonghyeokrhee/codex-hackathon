from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
PIPELINE_PATH = SRC_DIR / "cs_pipeline.py"
DEMO_PATH = SRC_DIR / "cs_demo.py"
FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "cs_seed.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class CsPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = load_module(PIPELINE_PATH, "cs_pipeline")

    def test_loads_and_normalizes_seed_tickets(self):
        raw_tickets = self.pipeline.load_seed_tickets(FIXTURE_PATH)
        normalized = [
            self.pipeline.normalize_ticket(raw_ticket, index + 1)
            for index, raw_ticket in enumerate(raw_tickets)
        ]

        self.assertEqual(len(normalized), 4)
        self.assertEqual(normalized[1].title, "The report filter label is confusing")
        self.assertEqual(normalized[1].customer, "Northwind")
        self.assertEqual(normalized[2].content, "The payment flow throws a 500 error and the order never completes. This blocks customers from finishing the purchase.")

    def test_classifies_scope_and_routes_deterministically(self):
        report = self.pipeline.run_pipeline(FIXTURE_PATH)
        by_ticket = {item.ticket_id: item for item in report.tickets}

        self.assertEqual(by_ticket["seed-1"].category, "FAQ")
        self.assertEqual(by_ticket["seed-1"].scope_label, "P2")
        self.assertEqual(by_ticket["seed-1"].route, "Customer Reply Draft")

        self.assertEqual(by_ticket["seed-2"].category, "UX_GAP")
        self.assertEqual(by_ticket["seed-2"].scope_label, "P2")
        self.assertEqual(by_ticket["seed-2"].route, "UX Review")
        self.assertTrue(by_ticket["seed-2"].codex_pr_candidate)

        self.assertEqual(by_ticket["seed-3"].category, "DEFECT")
        self.assertEqual(by_ticket["seed-3"].severity, "HIGH")
        self.assertEqual(by_ticket["seed-3"].route, "Hotfix Queue")

        self.assertEqual(by_ticket["seed-4"].category, "DEFECT")
        self.assertEqual(by_ticket["seed-4"].severity, "MEDIUM")
        self.assertEqual(by_ticket["seed-4"].scope_label, "P1")
        self.assertEqual(by_ticket["seed-4"].route, "Sprint Backlog")

    def test_cli_writes_markdown_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "demo-report.md"
            subprocess.run(
                [
                    sys.executable,
                    str(DEMO_PATH),
                    str(FIXTURE_PATH),
                    "--output",
                    str(output_path),
                ],
                check=True,
                cwd=ROOT,
            )

            report_text = output_path.read_text(encoding="utf-8")

        self.assertIn("# CS triage demo report", report_text)
        self.assertIn("seed-3", report_text)
        self.assertIn("Hotfix Queue", report_text)
        self.assertIn("Codex PR candidate: yes", report_text)


if __name__ == "__main__":
    unittest.main()
