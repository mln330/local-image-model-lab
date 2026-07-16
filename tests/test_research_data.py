from __future__ import annotations

import csv
import hashlib
import json
import re
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
            "flux2-klein-crayon-holders-lifestyle.jpg",
            "planter-private",
        }
        searchable = [ROOT / "README.md", ROOT / "ARTICLE.md"]
        searchable.extend((ROOT / "docs").glob("*.md"))
        searchable.extend((ROOT / "data").glob("*.json"))
        combined = "\n".join(path.read_text(encoding="utf-8") for path in searchable)

        self.assertEqual({value for value in retired if value in combined}, set())

    def test_featured_flux_output_matches_audited_provenance(self) -> None:
        manifest = json.loads(
            (ROOT / "data" / "followup-runs-2026-07-15.json").read_text(
                encoding="utf-8"
            )
        )
        run = next(
            item
            for item in manifest["runs"]
            if item["id"] == "flux-sign-scale-context-historical"
        )
        output = (ROOT / run["output"]).read_bytes()

        self.assertEqual(hashlib.sha256(output).hexdigest(), run["published_sha256"])
        self.assertEqual(run["source_sha256"], manifest["sources"][run["source"]]["published_sha256"])
        self.assertEqual(run["raw_output_sha256"], "cc610cde7029e1ec7ca4ca7d6896080e4cb088ffe3285e4278452214f89682ea")
        self.assertEqual(run["seed"], 12100002)
        self.assertIn("scale-context product photo", run["prompt"])

    def test_selected_gallery_outputs_match_audited_provenance(self) -> None:
        manifest = json.loads(
            (ROOT / "data" / "followup-runs-2026-07-15.json").read_text(
                encoding="utf-8"
            )
        )
        expected_hashes = {
            "flux-rocket-themed-room-selected": "4e25805dc4feff75014bf681aa6a0bb21b00094805d1f4c37aa1e931046f729e",
            "flux-rocket-classroom-desk-selected": "f4857925a0f79ac6059be80aeede4c226905f63177e3d9ee55f2fda029d59eee",
            "flux-rocket-craft-desk-selected": "ab8a04320d1600b33c8989ef00e50c8e90ae2aa21267d77d8aea328c95117060",
            "flux-unicorn-styled-vignette-selected": "8a1e20369316f62de2c9ad31dec56bda45c1cd8c328659db6c58fdb59f8b09c9",
            "flux-unicorn-room-context-selected": "b5c7ffcb3c4f6960862bda72e7898dda6668e5d2406209b76a096476b531ebb0",
            "flux-owl-homework-desk-selected": "6bd242bb50829ae00b732dece3b6cc8453e393cf4f65368af97a749c2c81bcbc",
            "flux-owl-everyday-desk-selected": "74f74fc114d9b96562a0ddbc1453fe2e7a401d34b93a0e2d29f8672c14842b3b",
            "flux-owl-classroom-vignette-selected": "b8c9aac236682561a28a2eb5aa013a4300411d24986b7c3cfca6cf4b4b137ef5",
            "qwen-sign-clean-hero-quality-target": "26581dcaa82969981e2395bae2e795d7fb7afcce998ef3318495a2c22b9bfc3c",
            "qwen-sign-room-lifestyle-quality-target": "fca875f3e8cdb19ddefb24b5ca4f74a06a2e1340484b9c9febb45118550c6e4e",
            "qwen-sign-gift-context-quality-target": "9ae661f176d0509d0a6e1e8246d9a8efb3556f314c0841d0fcc6f7647806eac5",
        }
        runs = {run["id"]: run for run in manifest["runs"]}

        for run_id, expected_hash in expected_hashes.items():
            run = runs[run_id]
            actual_hash = hashlib.sha256((ROOT / run["output"]).read_bytes()).hexdigest()
            self.assertEqual(actual_hash, expected_hash, run_id)
            self.assertEqual(run["published_sha256"], expected_hash, run_id)

    def test_every_article_image_has_a_provenance_record(self) -> None:
        manifest = json.loads(
            (ROOT / "data" / "followup-runs-2026-07-15.json").read_text(
                encoding="utf-8"
            )
        )
        published_docs = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in ("ARTICLE.md", "README.md")
        )
        article_assets = set(re.findall(r"\]\((assets/[^)]+)\)", published_docs))
        article_assets.update(
            re.findall(r'<img[^>]+src="(assets/[^"]+)"', published_docs)
        )
        documented_assets = {
            source["published_path"] for source in manifest["sources"].values()
        }
        documented_assets.update(
            run["output"] for run in manifest["runs"] if "output" in run
        )

        self.assertEqual(article_assets - documented_assets, set())

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
