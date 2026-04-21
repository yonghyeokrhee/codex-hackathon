from __future__ import annotations

from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "docs" / "cs_triage_rules.md"
BOUNDARY_FIXTURE_PATH = ROOT / "tests" / "fixtures" / "cs_triage_boundary_cases.json"
SKILL_PATH = Path("/Users/yong/.codex/skills/cs-triage/SKILL.md")
SUPPORT_SKILL_PATH = Path("/Users/yong/.codex/skills/support-center/SKILL.md")
CODEBASE_SKILL_PATH = Path("/Users/yong/.codex/skills/mop-codebase-triage/SKILL.md")
MOP_FE_AGENTS_PATH = Path("/Users/yong/mop-fe/AGENTS.md")
MOP_BE_AGENTS_PATH = Path("/Users/yong/mop-be/AGENTS.md")
AUTOMATION_PATH = Path("/Users/yong/.codex/automations/cs/automation.toml")
MEMORY_PATH = Path("/Users/yong/.codex/automations/cs/memory.md")


class CsTriageAssetTests(unittest.TestCase):
    def test_rules_doc_maps_spec_requirements(self):
        text = RULES_PATH.read_text(encoding="utf-8")

        self.assertIn("FAQ 가능성 확인 -> support 문서 조회 -> 부족하면 코드베이스 탐색 -> UX_GAP/DEFECT 판정 -> P1/P2 부여", text)
        self.assertIn("https://support.mop.co.kr/", text)
        self.assertIn("/Users/yong/mop-fe", text)
        self.assertIn("/Users/yong/mop-be", text)
        self.assertIn("UX_GAP", text)
        self.assertIn("DEFECT", text)
        self.assertIn("P1", text)
        self.assertIn("P2", text)
        self.assertIn("evidence", text)
        self.assertIn("rationale", text)
        self.assertIn("fallback", text)
        self.assertIn("#cs-intake", text)
        self.assertIn("즉시 답변", text)

    def test_skill_reads_rules_doc_and_emits_required_outputs(self):
        text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn("description: Use when", text)
        self.assertIn("/Users/yong/codex-hackathon/docs/cs_triage_rules.md", text)
        self.assertIn("/Users/yong/.codex/skills/support-center/SKILL.md", text)
        self.assertIn("https://support.mop.co.kr/", text)
        self.assertIn("/Users/yong/mop-fe", text)
        self.assertIn("/Users/yong/mop-be", text)
        self.assertIn("/Users/yong/.codex/skills/mop-codebase-triage/SKILL.md", text)
        self.assertIn("FAQ", text)
        self.assertIn("UX_GAP", text)
        self.assertIn("DEFECT", text)
        self.assertIn("reply_draft", text)
        self.assertIn("operator_note", text)
        self.assertIn("next_action", text)
        self.assertIn("#cs-intake", text)

    def test_support_center_skill_provides_cs_reply_workflow(self):
        text = SUPPORT_SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn("description: Use when", text)
        self.assertIn("https://support.mop.co.kr/", text)
        self.assertIn("reply_draft", text)
        self.assertIn("support_evidence", text)
        self.assertIn("confidence", text)
        self.assertIn("operator_note", text)
        self.assertIn("CS response tone", text)
        self.assertIn("do not guess", text.lower())
        self.assertIn("fallback", text.lower())

    def test_mop_codebase_skill_uses_agents_context_and_outputs_triage_fields(self):
        text = CODEBASE_SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn("description: Use when", text)
        self.assertIn("/Users/yong/mop-fe/AGENTS.md", text)
        self.assertIn("/Users/yong/mop-be/AGENTS.md", text)
        self.assertIn("UX_GAP", text)
        self.assertIn("DEFECT", text)
        self.assertIn("reply_draft", text)
        self.assertIn("operator_note", text)
        self.assertIn("next_action", text)
        self.assertIn("subagent", text.lower())
        self.assertIn("evidence", text)

    def test_mop_fe_and_be_agents_docs_exist_for_source_context(self):
        fe_text = MOP_FE_AGENTS_PATH.read_text(encoding="utf-8")
        be_text = MOP_BE_AGENTS_PATH.read_text(encoding="utf-8")

        self.assertIn("CS triage", fe_text)
        self.assertIn("UX_GAP", fe_text)
        self.assertIn("DEFECT", fe_text)
        self.assertIn("/Users/yong/mop-be", fe_text)

        self.assertIn("CS triage", be_text)
        self.assertIn("UX_GAP", be_text)
        self.assertIn("DEFECT", be_text)
        self.assertIn("controller", be_text.lower())

    def test_automation_prompt_requires_rules_doc_and_skill(self):
        text = AUTOMATION_PATH.read_text(encoding="utf-8")

        self.assertIn("docs/cs_triage_rules.md", text)
        self.assertIn("cs-triage", text)
        self.assertIn("support-center", text)
        self.assertIn("mop-codebase-triage", text)
        self.assertIn("/Users/yong/mop-fe/AGENTS.md", text)
        self.assertIn("/Users/yong/mop-be/AGENTS.md", text)
        self.assertIn("https://support.mop.co.kr/", text)
        self.assertIn("/Users/yong/mop-fe", text)
        self.assertIn("/Users/yong/mop-be", text)
        self.assertIn("FAQ / UX_GAP / DEFECT", text)
        self.assertIn("P1 / P2", text)
        self.assertIn("reply_draft", text)
        self.assertIn("operator_note", text)
        self.assertIn("#cs-intake", text)
        self.assertIn("support center", text.lower())
        self.assertIn("subagent", text.lower())

    def test_memory_template_tracks_triage_decisions(self):
        text = MEMORY_PATH.read_text(encoding="utf-8")

        self.assertIn("support", text.lower())
        self.assertIn("codebase", text.lower())
        self.assertIn("subagent", text.lower())
        self.assertIn("fallback", text.lower())
        self.assertIn("cs-intake", text.lower())
        self.assertIn("FAQ", text)
        self.assertIn("UX_GAP", text)
        self.assertIn("DEFECT", text)

    def test_boundary_fixture_covers_required_triage_paths(self):
        data = json.loads(BOUNDARY_FIXTURE_PATH.read_text(encoding="utf-8"))
        cases = data["cases"]
        by_expected = {(case["expected_category"], case["expected_scope_label"]) for case in cases}

        self.assertIn(("FAQ", "P2"), by_expected)
        self.assertIn(("UX_GAP", "P2"), by_expected)
        self.assertIn(("DEFECT", "P1"), by_expected)


if __name__ == "__main__":
    unittest.main()
