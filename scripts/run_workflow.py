#!/usr/bin/env python3
"""Run a parameterized ComfyUI API workflow using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any


PLACEHOLDER = re.compile(r"^\{\{([A-Z0-9_]+)\}\}$")


def parse_value(value: str) -> Any:
    """Preserve numbers, booleans, arrays, and objects passed through --set."""
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def parse_assignments(items: list[str]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Expected KEY=VALUE, received: {item}")
        key, value = item.split("=", 1)
        key = key.strip().upper()
        if not key:
            raise ValueError(f"Empty key in assignment: {item}")
        values[key] = parse_value(value)
    return values


def replace_placeholders(value: Any, replacements: dict[str, Any]) -> Any:
    if isinstance(value, dict):
        return {key: replace_placeholders(item, replacements) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_placeholders(item, replacements) for item in value]
    if not isinstance(value, str):
        return value

    whole = PLACEHOLDER.match(value)
    if whole:
        key = whole.group(1)
        return replacements.get(key, value)

    result = value
    for key, replacement in replacements.items():
        result = result.replace(f"{{{{{key}}}}}", str(replacement))
    return result


def unresolved_placeholders(value: Any) -> set[str]:
    encoded = json.dumps(value)
    return set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", encoded))


def request_json(url: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data)
    if data is not None:
        request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {error.code} from {url}: {body}") from error


def upload_image(server: str, image_path: Path) -> str:
    boundary = f"----local-image-model-lab-{uuid.uuid4().hex}"
    content_type = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
    parts: list[bytes] = []

    def add_field(name: str, value: str) -> None:
        parts.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                value.encode(),
                b"\r\n",
            ]
        )

    add_field("type", "input")
    add_field("overwrite", "true")
    parts.extend(
        [
            f"--{boundary}\r\n".encode(),
            (
                f'Content-Disposition: form-data; name="image"; '
                f'filename="{image_path.name}"\r\n'
            ).encode(),
            f"Content-Type: {content_type}\r\n\r\n".encode(),
            image_path.read_bytes(),
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )

    request = urllib.request.Request(
        f"{server}/upload/image",
        data=b"".join(parts),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Image upload failed: HTTP {error.code}: {body}") from error

    name = result["name"]
    subfolder = result.get("subfolder", "").strip("/\\")
    return f"{subfolder}/{name}" if subfolder else name


def wait_for_history(server: str, prompt_id: str, timeout_seconds: float) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        history = request_json(f"{server}/history/{urllib.parse.quote(prompt_id)}")
        if prompt_id in history:
            result = history[prompt_id]
            status = result.get("status", {})
            if status.get("status_str") == "error":
                raise RuntimeError(json.dumps(status, indent=2))
            return result
        time.sleep(0.5)
    raise TimeoutError(f"Prompt {prompt_id} did not finish within {timeout_seconds} seconds")


def download_outputs(server: str, history: dict[str, Any], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[Path] = []
    for node_id, node_output in history.get("outputs", {}).items():
        for index, image in enumerate(node_output.get("images", [])):
            query = urllib.parse.urlencode(
                {
                    "filename": image["filename"],
                    "subfolder": image.get("subfolder", ""),
                    "type": image.get("type", "output"),
                }
            )
            suffix = Path(image["filename"]).suffix or ".png"
            destination = output_dir / f"{node_id}-{index}{suffix}"
            urllib.request.urlretrieve(f"{server}/view?{query}", destination)
            downloaded.append(destination)
    return downloaded


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--server", default="http://127.0.0.1:8188")
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument("--timeout", type=float, default=900)
    parser.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Replace a workflow placeholder. May be specified multiple times.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.template.is_file():
        raise FileNotFoundError(args.template)
    if not args.image.is_file():
        raise FileNotFoundError(args.image)

    server = args.server.rstrip("/")
    replacements = parse_assignments(args.set)
    replacements.update(
        {
            "PROMPT": args.prompt,
            "NEGATIVE_PROMPT": args.negative_prompt,
            "PRODUCT_IMAGE": upload_image(server, args.image),
        }
    )
    replacements.setdefault("OUTPUT_PREFIX", "local-image-model-lab/run")

    template = json.loads(args.template.read_text(encoding="utf-8"))
    workflow = replace_placeholders(template, replacements)
    unresolved = sorted(unresolved_placeholders(workflow))
    if unresolved:
        raise ValueError("Missing replacements: " + ", ".join(unresolved))

    started = time.perf_counter()
    queued = request_json(
        f"{server}/prompt",
        {"prompt": workflow, "client_id": uuid.uuid4().hex},
    )
    prompt_id = queued["prompt_id"]
    history = wait_for_history(server, prompt_id, args.timeout)
    outputs = download_outputs(server, history, args.output_dir)
    elapsed = time.perf_counter() - started

    print(
        json.dumps(
            {
                "prompt_id": prompt_id,
                "elapsed_seconds": round(elapsed, 3),
                "outputs": [str(path.resolve()) for path in outputs],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, TimeoutError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
