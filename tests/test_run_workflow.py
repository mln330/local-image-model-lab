from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_workflow.py"
SPEC = importlib.util.spec_from_file_location("run_workflow", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
RUN_WORKFLOW = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUN_WORKFLOW)


class WorkflowTemplateTests(unittest.TestCase):
    def test_parse_assignments_preserves_types(self) -> None:
        result = RUN_WORKFLOW.parse_assignments(
            ["STEPS=2", "CFG=1.0", "ENABLED=true", "NAME=model.safetensors"]
        )

        self.assertEqual(result["STEPS"], 2)
        self.assertEqual(result["CFG"], 1.0)
        self.assertIs(result["ENABLED"], True)
        self.assertEqual(result["NAME"], "model.safetensors")

    def test_whole_placeholder_keeps_non_string_type(self) -> None:
        template = {"inputs": {"steps": "{{STEPS}}", "cfg": "{{CFG}}"}}
        result = RUN_WORKFLOW.replace_placeholders(template, {"STEPS": 4, "CFG": 1.0})

        self.assertEqual(result["inputs"]["steps"], 4)
        self.assertEqual(result["inputs"]["cfg"], 1.0)

    def test_embedded_placeholder_becomes_text(self) -> None:
        result = RUN_WORKFLOW.replace_placeholders(
            "result/{{ROUTE}}/run", {"ROUTE": "qwen"}
        )

        self.assertEqual(result, "result/qwen/run")

    def test_unresolved_placeholders_are_reported(self) -> None:
        unresolved = RUN_WORKFLOW.unresolved_placeholders(
            {"a": "{{MODEL}}", "b": ["{{SEED}}", 1]}
        )

        self.assertEqual(unresolved, {"MODEL", "SEED"})

    def test_invalid_assignment_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            RUN_WORKFLOW.parse_assignments(["MISSING_SEPARATOR"])


if __name__ == "__main__":
    unittest.main()
