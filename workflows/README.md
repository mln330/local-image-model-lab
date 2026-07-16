# ComfyUI API workflow templates

These files are parameterized **API-format** ComfyUI graphs. They are intended for scripted execution, not direct drag-and-drop into the visual editor.

## Templates

### `flux2-klein-4b-text-to-image-api.json`

This graph uses the same distilled FLUX.2 Klein 4B stack as the practical
editing route, but starts from an empty latent. It is useful for generating
synthetic demonstration inputs and original visual concepts without publishing
private source material. Core placeholders are `WIDTH`, `HEIGHT`, `STEPS`,
`CFG`, `PROMPT`, and `SEED` plus the shared model filenames.

### `qwen-image-edit-lightning-api.json`

Core placeholders:

| Placeholder | Example from the experiment |
|---|---|
| `DIFFUSION_MODEL` | `qwen_image_edit_2511_fp8mixed.safetensors` |
| `TEXT_ENCODER` | `qwen_2.5_vl_7b_fp8_scaled.safetensors` |
| `VAE_MODEL` | `qwen_image_vae.safetensors` |
| `LORA_NAME` | `Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors` |
| `LORA_STRENGTH` | `1.0` |
| `STEPS` | `2` |
| `CFG` | `1.0` |
| `DENOISE` | `0.85` |

The included graph uses `FluxKontextImageScale`, which selects a compatible working size from the source aspect ratio. The 640-specific benchmark used a separate fixed `ImageScale` graph and is not represented by this template.

### `flux2-klein-4b-edit-api.json`

Core placeholders:

| Placeholder | Example from the practical default |
|---|---|
| `DIFFUSION_MODEL` | `flux-2-klein-4b-fp8.safetensors` |
| `TEXT_ENCODER` | `qwen_3_4b_fp4_flux2.safetensors` |
| `VAE_MODEL` | `flux2-vae.safetensors` |
| `MEGAPIXELS` | `0.8` |
| `STEPS` | `6` |
| `CFG` | `1.0` |

Use this as the practical default for fast scene generation when no new exact scene text is required. NVFP4 filenames and nodes depend on the distribution you install; do not assume an FP8 graph and an NVFP4 custom-node graph are interchangeable.

## Shared editing placeholders

The image-edit templates also require:

- `PRODUCT_IMAGE`
- `PROMPT`
- `NEGATIVE_PROMPT`
- `SEED`
- `OUTPUT_PREFIX`

The text-to-image graph does not require `PRODUCT_IMAGE` or
`NEGATIVE_PROMPT`.

[`scripts/generate_article_examples.py`](../scripts/generate_article_examples.py)
shows the text-to-image graph and editing graph used together to create,
compare, and time the synthetic use-case demonstrations.

[`scripts/run_workflow.py`](../scripts/run_workflow.py) fills the image and prompt placeholders and accepts the remaining values through repeated `--set KEY=VALUE` arguments.

## Security

ComfyUI's API is a trusted local worker interface. Do not expose it directly to the public internet. Place authentication, file validation, queue limits, retention policy, and model allowlists in a service boundary in front of it.
