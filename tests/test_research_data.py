from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ResearchDataTests(unittest.TestCase):
    def test_recommended_routes_match_documented_decision(self) -> None:
        with (ROOT / "data" / "quality-tiers.csv").open(
            newline="", encoding="utf-8"
        ) as stream:
            rows = list(csv.DictReader(stream))

        by_decision = {row["decision"]: row for row in rows}
        self.assertIn("FLUX.2 Klein", by_decision["Practical default"]["configuration"])
        self.assertIn("Native Qwen", by_decision["Quality favorite"]["configuration"])
        self.assertIn("Nunchaku", by_decision["Tested not selected"]["configuration"])

    def test_every_recommended_sample_exists(self) -> None:
        with (ROOT / "data" / "quality-tiers.csv").open(
            newline="", encoding="utf-8"
        ) as stream:
            rows = csv.DictReader(stream)
            missing = [row["sample"] for row in rows if not (ROOT / row["sample"]).is_file()]

        self.assertEqual(missing, [])

    def test_followup_manifest_outputs_exist(self) -> None:
        manifest = json.loads(
            (ROOT / "data" / "followup-runs-2026-07-15.json").read_text(
                encoding="utf-8"
            )
        )
        missing = [
            run["output"]
            for run in manifest["runs"]
            if "output" in run and not (ROOT / run["output"]).is_file()
        ]

        self.assertEqual(missing, [])

    def test_published_sources_have_explicit_provenance(self) -> None:
        manifest = json.loads(
            (ROOT / "data" / "followup-runs-2026-07-15.json").read_text(
                encoding="utf-8"
            )
        )
        allowed_kinds = set(manifest["source_policy"]["classes"])

        self.assertGreaterEqual(len(manifest["sources"]), 7)
        for source in manifest["sources"].values():
            self.assertIn(source["kind"], allowed_kinds)
            self.assertTrue((ROOT / source["published_path"]).is_file())

    def test_use_case_gallery_has_source_and_result_for_every_category(self) -> None:
        pairs = [
            (
                "assets/sources/restoration-synthetic-damaged-scan.png",
                "assets/results/qwen-restoration-synthetic-scan.png",
            ),
            (
                "assets/sources/game-concept-beetle-lantern-sketch.png",
                "assets/results/flux2-klein-game-concept-beetle-lantern.png",
            ),
            (
                "assets/sources/synthetic-data-valve-reference.png",
                "assets/results/flux2-klein-synthetic-data-valve.png",
            ),
            (
                "assets/sources/confidential-design-headphone-stand-sketch.png",
                "assets/results/flux2-klein-confidential-design-headphone-stand.png",
            ),
            (
                "assets/sources/presentation-energy-flow-sketch.png",
                "assets/results/flux2-klein-presentation-energy-flow.png",
            ),
            (
                "assets/sources/offline-creative-lighthouse-drawing.png",
                "assets/results/flux2-klein-offline-creative-lighthouse.png",
            ),
        ]

        missing = [path for pair in pairs for path in pair if not (ROOT / path).is_file()]
        self.assertEqual(missing, [])

    def test_retired_or_third_party_examples_are_not_referenced(self) -> None:
        retired = {
            "qwen-private-photo-cleanup.png",
            "flux2-klein-game-asset.png",
            "flux2-klein-synthetic-data.png",
            "flux2-klein-rocket-lifestyle.png",
            "planter-private",
        }
        searchable = [ROOT / "README.md", ROOT / "ARTICLE.md"]
        searchable.extend((ROOT / "docs").glob("*.md"))
        searchable.extend((ROOT / "data").glob("*.json"))
        combined = "\n".join(path.read_text(encoding="utf-8") for path in searchable)

        self.assertEqual({value for value in retired if value in combined}, set())

    def test_warm_flux_followups_are_interactive(self) -> None:
        manifest = json.loads(
            (ROOT / "data" / "followup-runs-2026-07-15.json").read_text(
                encoding="utf-8"
            )
        )
        warm_flux = [
            run
            for run in manifest["runs"]
            if run["model"].startswith("FLUX.2")
            and run["timing_class"].startswith("warm")
        ]

        self.assertGreaterEqual(len(warm_flux), 2)
        self.assertTrue(all(run["elapsed_seconds"] < 10 for run in warm_flux))

    def test_gpu_price_ranges_are_ordered(self) -> None:
        with (ROOT / "data" / "gpu-price-snapshot-2026-07-15.csv").open(
            newline="", encoding="utf-8"
        ) as stream:
            rows = list(csv.DictReader(stream))

        self.assertGreaterEqual(len(rows), 8)
        for row in rows:
            self.assertLessEqual(
                float(row["observed_price_low_usd"]),
                float(row["observed_price_high_usd"]),
                row["gpu"],
            )


if __name__ == "__main__":
    unittest.main()
