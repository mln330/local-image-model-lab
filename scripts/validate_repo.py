#!/usr/bin/env python3
"""Validate repository data, local Markdown links, and public-content hygiene."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def validate_json(errors: list[str]) -> None:
    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {error}")


def validate_csv(errors: list[str]) -> None:
    for path in ROOT.rglob("*.csv"):
        with path.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.reader(stream))
        if not rows:
            errors.append(f"{path.relative_to(ROOT)}: empty CSV")
            continue
        width = len(rows[0])
        for line_number, row in enumerate(rows[1:], start=2):
            if len(row) != width:
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number}: "
                    f"expected {width} columns, found {len(row)}"
                )


def validate_markdown_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(content):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            target = target.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            candidate = (path.parent / urllib_unquote(target)).resolve()
            if not candidate.exists():
                errors.append(
                    f"{path.relative_to(ROOT)}: missing local link target: {target}"
                )


def urllib_unquote(value: str) -> str:
    from urllib.parse import unquote

    return unquote(value)


def validate_public_content(errors: list[str]) -> None:
    extensions = {".md", ".json", ".csv"}
    forbidden = {
        "c:\\users\\": "absolute Windows user path",
        "shopspark": "unrelated private project name",
    }
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        content = path.read_text(encoding="utf-8").lower()
        for text, description in forbidden.items():
            if text in content:
                errors.append(f"{path.relative_to(ROOT)}: contains {description}")


def validate_asset_metadata(errors: list[str]) -> None:
    for path in (ROOT / "assets").rglob("*"):
        if not path.is_file():
            continue
        data = path.read_bytes()
        suffix = path.suffix.lower()
        if suffix == ".png" and any(chunk in data for chunk in (b"tEXt", b"zTXt", b"iTXt")):
            errors.append(f"{path.relative_to(ROOT)}: contains PNG text metadata")
        if suffix in {".jpg", ".jpeg"} and (
            b"Exif\x00\x00" in data or b"http://ns.adobe.com/xap/1.0/" in data
        ):
            errors.append(f"{path.relative_to(ROOT)}: contains JPEG EXIF/XMP metadata")


def main() -> int:
    errors: list[str] = []
    validate_json(errors)
    validate_csv(errors)
    validate_markdown_links(errors)
    validate_public_content(errors)
    validate_asset_metadata(errors)

    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
