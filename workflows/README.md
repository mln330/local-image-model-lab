# ComfyUI API workflow templates

These files are parameterized **API-format** ComfyUI graphs. They are intended for scripted execution, not direct drag-and-drop into the visual editor.

## Templates

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

### `nunchaku-qwen-image-edit-api.json`

Core placeholders:

| Placeholder | Example from the best observed run |
|---|---|
| `DIFFUSION_MODEL` | `nunchaku_qwen_image_edit_2511_ultimate_speed_fp4.safetensors` |
| `TEXT_ENCODER` | `qwen_2.5_vl_7b_fp8_scaled.safetensors` |
| `VAE_MODEL` | `qwen_image_vae.safetensors` |
| `LORA_NAME` | `Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors` |
| `MEGAPIXELS` | `0.8` |
| `STEPS` | `4` |
| `CFG` | `1.0` |
| `DENOISE` | `1.0` |
| `CPU_OFFLOAD` | `auto` |
| `NUM_BLOCKS_ON_GPU` | `60` |
| `USE_PIN_MEMORY` | `disable` |
| `LORA_CPU_OFFLOAD` | `auto` |

The exact `ultimate_speed` checkpoint used in the experiment was published by QuantFunc and is a community Nunchaku-compatible quantization, not an official Nunchaku release. Review both the [model card](https://huggingface.co/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511) and runtime compatibility before use.

### `flux2-klein-4b-edit-api.json`

Core placeholders:

| Placeholder | Example from the Great B run |
|---|---|
| `DIFFUSION_MODEL` | `flux-2-klein-4b-fp8.safetensors` |
| `TEXT_ENCODER` | `qwen_3_4b_fp4_flux2.safetensors` |
| `VAE_MODEL` | `flux2-vae.safetensors` |
| `MEGAPIXELS` | `0.8` |
| `STEPS` | `6` |
| `CFG` | `1.0` |

NVFP4 filenames depend on the distribution you install. Do not assume an FP8 graph and an NVFP4 custom-node graph are interchangeable.

## Shared placeholders

All templates also require:

- `PRODUCT_IMAGE`
- `PROMPT`
- `NEGATIVE_PROMPT`
- `SEED`
- `OUTPUT_PREFIX`

[`scripts/run_workflow.py`](../scripts/run_workflow.py) fills the image and prompt placeholders and accepts the remaining values through repeated `--set KEY=VALUE` arguments.

## Security

ComfyUI's API is a trusted local worker interface. Do not expose it directly to the public internet. Place authentication, file validation, queue limits, retention policy, and model allowlists in a service boundary in front of it.
