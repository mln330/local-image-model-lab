"""Generate traceable FLUX.2 Klein candidates for the article use-case gallery."""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

from PIL import Image, ImageDraw


MODEL = "flux-2-klein-4b-fp8.safetensors"
TEXT_ENCODER = "qwen_3_4b_fp4_flux2.safetensors"
VAE = "flux2-vae.safetensors"
BASE_SEED = 71526000

ROCKET_PROMPTS = [
    "Create a premium lifestyle product photograph of the exact 3D-printed rocket-shaped organizer in the reference. Preserve its cream body, red fins and top panel, black trim, orange flame, circular black window, visible print-layer texture, storage geometry, and all current pens. Place it on a tidy natural-wood art desk in a bright modern playroom, with a few colored pencils and one closed sketchbook arranged naturally. Soft morning window light from the left, convincing contact shadow, coherent reflections, shallow depth of field, airy editorial composition. The product is the clear focal point and fully visible at a natural three-quarter angle. Do not redesign, duplicate, stretch, or crop the organizer. No text, labels, badges, hands, people, or extra containers.",
    "Create an elegant catalog lifestyle photo of the exact rocket organizer from the reference. Preserve every product color, black outline, circular window, red fins, orange flame, print texture, proportions, and the same contents. Stage it naturally on a pale oak desk beside a small stack of blank drawing paper and three colored pencils in a sunlit children's art corner. Use balanced soft daylight, realistic contact and cast shadows, restrained props, gentle background blur, and generous negative space. Product fully visible, three-quarter view, believable scale. No text, logos, people, hands, duplicate products, invented openings, or changed geometry.",
    "Create a polished hero photograph of the exact 3D-printed rocket pen organizer from the reference. Preserve the cream, red, black, and orange design, circular black window, fin shapes, printed texture, top opening, proportions, and all pens. Place it on a clean warm-white studio sweep with a subtle pale-blue backdrop, one soft key light and natural fill, precise contact shadow, crisp edge detail, premium marketplace photography, complete silhouette visible. No decorative scene, text, labels, hands, people, duplicates, or product redesign.",
    "Create a bright imaginative product photograph of the exact rocket organizer from the reference without changing it. Preserve all colors, outlines, fins, window, flame, dimensions, print layers, and current contents. Put it on a clean craft table in a tasteful space-themed reading nook with a small blank notebook and a few crayons, softly blurred planets as wall decor far behind. Natural daylight, realistic grounding shadow, subtle depth of field, calm composition, no clutter. No text, people, hands, duplicate containers, extra openings, or altered product geometry.",
]

USE_CASES = {
    "restoration": {
        "source": "A convincing synthetic scan of a 1940s black-and-white photograph showing a small Art Deco railway depot from the street, no people and no readable signs. The old print is badly faded with paper creases, dust, scratches, a torn upper corner, silvering at the edges, and uneven exposure. Flatbed scanner framing, authentic archival paper texture, documentary composition.",
        "edit": "Restore this exact archival railway-depot photograph while preserving the architecture, camera position, monochrome character, period details, and original composition. Repair tears, creases, scratches, dust, edge silvering, fading, and uneven exposure. Recover plausible tonal detail without colorizing, modernizing, sharpening into halos, changing the building, adding people, or inventing readable signs. The result should look like a careful high-resolution museum scan of the same physical photograph.",
    },
    "game-concept": {
        "source": "A rough but readable pencil-and-marker concept sketch on white paper of a whimsical beetle-shaped fantasy lantern: rounded brass shell, two small folded wings, short curled legs forming a base, a teal glass abdomen that glows, and a loop handle. One three-quarter view, loose construction lines, no words or labels, photographed evenly from above.",
        "edit": "Turn this exact beetle-lantern concept into a polished isometric game inventory prop. Preserve the rounded brass shell, paired folded wings, curled-leg base, loop handle, proportions, and glowing teal glass abdomen. Stylized hand-painted 3D materials, crisp readable silhouette, subtle wear, warm brass highlights, soft oval grounding shadow, neutral charcoal studio background, production-ready fantasy-adventure concept art. Object only. No interface, text, labels, watermark, extra wings, or redesign.",
    },
    "synthetic-data": {
        "source": "A clean reference photograph of a fictional compact industrial valve assembly on a light-gray seamless studio surface. Turquoise cast-metal body, orange five-spoke hand wheel, two silver pipe flanges, four black mounting feet, small pressure cap, no logo, no serial number. Complete object visible at a front three-quarter inspection angle under diffuse neutral light.",
        "edit": "Create a controlled test-set variant of this exact fictional valve assembly. Preserve the turquoise body, orange five-spoke wheel, silver flanges, four black feet, pressure cap, dimensions, and front three-quarter viewpoint. Mount it naturally on a dark workshop bench under a single cool overhead utility light, with realistic low-light sensor noise, moderate background clutter kept out of focus, coherent metal reflections, and a complete visible silhouette. Do not change or duplicate components. No text, logo, hands, people, steam, damage, or dramatic cinematic effects.",
    },
    "confidential-design": {
        "source": "A confidential-looking industrial-design marker sketch on off-white paper for a modular over-ear headphone charging stand. Slim arched support, circular weighted base, small removable charging puck nested in the base, subtle cable channel, asymmetrical cyan accent panel. One clear three-quarter concept view with faint construction lines, no readable notes, no brand logo.",
        "edit": "Render this exact headphone charging-stand concept as a polished preproduction industrial-design visualization. Preserve the slim arched support, circular weighted base, nested removable charging puck, cable channel, asymmetrical cyan accent panel, and overall proportions. Matte charcoal recycled polymer, satin aluminum support, restrained cyan light, soft neutral studio sweep, realistic materials, precise contact shadow, premium design-review render. No headphones, text, logo, extra controls, people, or redesign.",
    },
    "presentation-visual": {
        "source": "A rough whiteboard-style sketch of a simple residential energy flow: rooftop solar panels on a small house at left, a wall-mounted home battery in the middle, and a compact electric car charger at right, connected by three clear directional paths. Black marker with yellow and teal accents, no words, numbers, symbols, or labels, photographed straight on.",
        "edit": "Transform this exact energy-flow sketch into a clean professional isometric presentation illustration. Preserve the house with rooftop solar at left, home battery in the middle, car charger at right, and the same three directional connections. Crisp editorial vector-like forms, white background, charcoal outlines, teal and golden-yellow accents, generous blank space around each element for deterministic labels to be added later. No generated text, numbers, icons with letters, gradients, logos, people, or extra equipment.",
    },
    "offline-creative": {
        "source": "A charming child's crayon drawing on white paper: a red-and-white lighthouse on a small green island, deep blue waves, one tiny orange sailboat, a large yellow crescent moon, and five uneven stars. Visible wax crayon texture, slightly crooked shapes, simple composition, no text, photographed flat from above.",
        "edit": "Turn this exact child's lighthouse drawing into a polished storybook illustration while preserving the red-and-white lighthouse, green island, deep blue waves, tiny orange sailboat, yellow crescent moon, five stars, and their recognizable placement. Layered cut-paper and gouache style, warm moonlight, gentle wave depth, tactile handmade texture, whimsical but sophisticated children's-book art. Keep the child's composition and color choices clearly recognizable. No text, extra boats, people, logos, or photorealism.",
    },
}


def replace(value, values):
    if isinstance(value, dict):
        return {key: replace(child, values) for key, child in value.items()}
    if isinstance(value, list):
        return [replace(child, values) for child in value]
    if isinstance(value, str):
        if value.startswith("{{") and value.endswith("}}"):
            return values.get(value[2:-2], value)
        for key, replacement in values.items():
            value = value.replace("{{" + key + "}}", str(replacement))
    return value


def post_json(url, payload, timeout=60):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())


def get_json(url, timeout=60):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read())


def upload(server, path):
    boundary = "----LocalImageLab" + uuid.uuid4().hex
    body = b"".join(
        [
            f'--{boundary}\r\nContent-Disposition: form-data; name="overwrite"\r\n\r\ntrue\r\n'.encode(),
            f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="{path.name}"\r\nContent-Type: image/png\r\n\r\n'.encode(),
            path.read_bytes(),
            f"\r\n--{boundary}--\r\n".encode(),
        ]
    )
    request = urllib.request.Request(
        server + "/upload/image",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read())["name"]


def execute(server, graph, output_path, timeout=300):
    started = time.perf_counter()
    prompt_id = post_json(server + "/prompt", {"client_id": uuid.uuid4().hex, "prompt": graph})["prompt_id"]
    while True:
        history = get_json(server + "/history/" + prompt_id, timeout=30)
        if prompt_id in history and history[prompt_id].get("status", {}).get("completed"):
            item = history[prompt_id]
            break
        if time.perf_counter() - started > timeout:
            raise TimeoutError(prompt_id)
        time.sleep(0.5)
    if item["status"]["status_str"] != "success":
        raise RuntimeError(json.dumps(item["status"], indent=2))
    image_info = next(iter(item["outputs"].values()))["images"][0]
    query = urllib.parse.urlencode(
        {
            "filename": image_info["filename"],
            "subfolder": image_info.get("subfolder", ""),
            "type": image_info.get("type", "output"),
        }
    )
    with urllib.request.urlopen(server + "/view?" + query, timeout=60) as response:
        output_path.write_bytes(response.read())
    return time.perf_counter() - started


def make_sheet(paths, output_path):
    cells = []
    for path in paths:
        image = Image.open(path).convert("RGB")
        image.thumbnail((420, 420), Image.Resampling.LANCZOS)
        cell = Image.new("RGB", (440, 470), "white")
        cell.paste(image, ((440 - image.width) // 2, 10))
        ImageDraw.Draw(cell).text((12, 438), path.stem, fill="black")
        cells.append(cell)
    columns = 2
    rows = (len(cells) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * 440, rows * 470), (232, 232, 232))
    for index, cell in enumerate(cells):
        sheet.paste(cell, ((index % columns) * 440, (index // columns) * 470))
    sheet.save(output_path, quality=92)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default="http://127.0.0.1:8000")
    parser.add_argument("--output", default=".research-output/article-examples-2026-07-15")
    parser.add_argument("--source-candidates", type=int, default=2)
    parser.add_argument("--edit-candidates", type=int, default=2)
    parser.add_argument("--rocket-candidates", type=int, default=4)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output = root / args.output
    output.mkdir(parents=True, exist_ok=True)
    t2i_template = json.loads((root / "workflows/flux2-klein-4b-text-to-image-api.json").read_text())
    edit_template = json.loads((root / "workflows/flux2-klein-4b-edit-api.json").read_text())
    records = []

    def t2i(name, prompt, seed):
        path = output / f"{name}.png"
        values = {
            "DIFFUSION_MODEL": MODEL,
            "TEXT_ENCODER": TEXT_ENCODER,
            "VAE_MODEL": VAE,
            "WIDTH": 912,
            "HEIGHT": 912,
            "STEPS": 6,
            "CFG": 1.0,
            "PROMPT": prompt,
            "SEED": seed,
            "OUTPUT_PREFIX": "local-image-model-lab/article/" + name,
        }
        seconds = execute(args.server, replace(t2i_template, values), path)
        records.append({"id": name, "kind": "text-to-image", "seed": seed, "seconds": round(seconds, 3), "prompt": prompt, "path": str(path.relative_to(root))})
        print(f"{name}: {seconds:.2f}s", flush=True)
        return path

    def edit(name, source, prompt, seed):
        path = output / f"{name}.png"
        values = {
            "PRODUCT_IMAGE": upload(args.server, source),
            "DIFFUSION_MODEL": MODEL,
            "TEXT_ENCODER": TEXT_ENCODER,
            "VAE_MODEL": VAE,
            "MEGAPIXELS": 0.8,
            "STEPS": 6,
            "CFG": 1.0,
            "PROMPT": prompt,
            "NEGATIVE_PROMPT": "",
            "SEED": seed,
            "OUTPUT_PREFIX": "local-image-model-lab/article/" + name,
        }
        seconds = execute(args.server, replace(edit_template, values), path)
        records.append({"id": name, "kind": "image-edit", "seed": seed, "seconds": round(seconds, 3), "prompt": prompt, "source": str(source.relative_to(root)), "path": str(path.relative_to(root))})
        print(f"{name}: {seconds:.2f}s", flush=True)
        return path

    rocket_source = root / "assets/sources/rocket-organizer-source.png"
    rocket_paths = []
    for index in range(args.rocket_candidates):
        rocket_paths.append(edit(f"rocket-listing-{index + 1}", rocket_source, ROCKET_PROMPTS[index % len(ROCKET_PROMPTS)], BASE_SEED + index))
    make_sheet(rocket_paths, output / "rocket-contact-sheet.jpg")

    for case_index, (name, prompts) in enumerate(USE_CASES.items()):
        sources = []
        for index in range(args.source_candidates):
            sources.append(t2i(f"{name}-source-{index + 1}", prompts["source"], BASE_SEED + 100 + case_index * 20 + index))
        edits = []
        for index in range(args.edit_candidates):
            edits.append(edit(f"{name}-result-{index + 1}", sources[0], prompts["edit"], BASE_SEED + 110 + case_index * 20 + index))
        make_sheet(sources + edits, output / f"{name}-contact-sheet.jpg")

    (output / "manifest.json").write_text(json.dumps(records, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
