# Methodology

## Research question

Can an RTX 5060 Ti 16 GB turn ordinary photos of physical products into attractive, source-faithful images with interactive warm latency, and which local route offers the best quality, speed, and operability for each type of edit?

## Test subject

The first stress-test source was a personalized rectangular children's room sign photographed on a granite counter.

It was selected because it combines several difficult requirements:

- exact personalized text (`ALEX'S ROOM`);
- recognizable astronaut, robot, moon, rocket, and planet artwork;
- a printed surface texture;
- fixed colors and layout;
- clear rounded-rectangle geometry;
- a source background that should not appear in the final scene.

A July 15 follow-up added an owned 3D-printed rocket-shaped pen organizer photographed against an ordinary fabric background. It contains no source lettering, which makes it a better test of scene generation without conflating composition quality with text rendering.

The two-product case study exposes useful failure modes but does not establish general performance across apparel, glass, jewelry, reflective metal, transparent objects, or human subjects.

## Requested image types

The repeatable prompt set covered:

1. clean studio hero;
2. room-use lifestyle scene;
3. scale context;
4. gift context;
5. detail/macro view.

The prompt always identified the preservation contract before describing the new scene. The important pattern was:

```text
Keep the exact product artwork, personalized text, shape, proportions,
colors, and printed texture unchanged. Change only the surrounding scene...
```

Prompt wording was adjusted for models with different instruction styles. The visual objective remained constant.

## Timing protocol

All reported times are end-to-end observations through the local ComfyUI API unless a row explicitly says otherwise. The measured interval begins when the prompt is queued and ends when the output is available from ComfyUI history.

The interval can include:

- model loading and offloading;
- source-image preprocessing;
- vision-language/text encoding;
- diffusion sampling;
- VAE encode/decode;
- output serialization.

Two timing classes are kept separate:

- **Cold:** first use after process start or model eviction.
- **Warm:** repeated use while the relevant graph components remain available.

Repeated-prompt and varied-prompt runs are also distinct. Repeating an identical prompt can benefit from conditioning caches and is not representative of a listing pipeline generating different asset types.

Times are rounded observations from exploratory runs, not statistically rigorous confidence intervals. The CSV preserves ranges where that is more honest than a false-precision average.

## Quality rubric

Each output was inspected at full resolution. Scores are subjective and designed to make the decision criteria explicit.

| Dimension | 1 | 5 | 10 |
|---|---|---|---|
| Identity fidelity | Different object | Recognizable with visible drift | Same product without meaningful drift |
| Text/art fidelity | Missing or invented | Partly readable/altered | Exact lettering and artwork |
| Physical integration | Obvious paste/artifacts | Plausible at a glance | Lighting, perspective, contact, scale, and shadows agree |
| Listing appeal | Unusable | Serviceable | Professional, clear, and persuasive |

An accepted route had to be useful for its declared purpose. A preview route could accept more identity risk if it was never treated as a publishable final. A fidelity route could use a simpler scene if it preserved the product reliably.

System preference also considered setup complexity, custom-runtime fragility, checkpoint provenance, and model-switch behavior. The strongest single image was not automatically the preferred operating route.

## Acceptance gates

### Publishable scene route

- warm end-to-end latency at or below 30 seconds;
- exact source text when the source contains contractual text;
- product silhouette and artwork remain recognizable;
- no obvious compositing edge, extra objects fused into the product, or impossible support;
- scene appropriate for the requested asset type;
- output useful at native resolution or after a separate upscale.

### Preview route

- warm latency near or below 10 seconds;
- composition useful for choosing a direction;
- identity drift clearly disclosed and checked before promotion to a final asset.

### Practical default route

- warm varied-prompt latency near or below 12 seconds;
- consistent visual appeal across more than one owned source;
- no dependence on a product-category-specific mode;
- setup and model provenance suitable for repeated operation;
- clear routing boundary for text-sensitive requests.

## Variables explored

- model family and checkpoint;
- native, FP8, FP4/NVFP4, INT4, and GGUF quantization paths;
- 0.45, 0.5, 0.8, 1.2, and approximately 2 MP output targets;
- one to 40 inference steps;
- Lightning/distilled adapters;
- denoise strength;
- CFG/guidance behavior;
- cold versus warm state;
- repeated versus varied prompts;
- ComfyUI memory modes and CPU offload;
- native Comfy nodes versus model-specific custom nodes.

## Threats to validity

- One GPU, operating system, driver stack, and source product.
- ComfyUI and custom nodes change frequently.
- Exploratory timing counts vary between configurations.
- Model licenses and recommended settings can change.
- Manual quality review is inherently subjective.
- Some configurations used community quantizations rather than official full-precision weights.
- A fast result at one aspect ratio does not predict all resolutions.

The output images are included so readers can disagree with the ratings.

## Recommended next experiment

Build a fixed 10-product corpus spanning text-heavy signs, jewelry, apparel, ceramics, glass, reflective metal, soft goods, art prints, irregular crafts, and products held by a person. Run accepted tiers with fixed seeds, three prompt types, and at least three warm repetitions. Add OCR, perceptual similarity, segmentation overlap, and blind human preference scoring.
