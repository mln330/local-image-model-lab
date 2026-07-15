# Reproducibility

## Scope

The included files reproduce the structure of the API workflows, not a one-click binary distribution. Model weights are not committed. ComfyUI and custom nodes evolve quickly, so exact versions must be recorded for any serious comparison.

## Baseline environment record

Record this information before running:

```text
Date:
Operating system:
GPU and VRAM:
NVIDIA/AMD/Intel driver:
Python:
PyTorch:
CUDA/ROCm/XPU runtime:
ComfyUI commit/version:
ComfyUI frontend version:
Custom node names and commits:
Launch arguments:
System RAM:
Source image hash:
```

The original test environment was Windows with an RTX 5060 Ti 16 GB and ComfyUI. It used normal dynamic model management; `--highvram` was explicitly rejected for the Qwen graph.

## Model placement

ComfyUI model paths vary by installation. Common directories include:

```text
ComfyUI/models/diffusion_models/
ComfyUI/models/text_encoders/
ComfyUI/models/vae/
ComfyUI/models/loras/
```

The workflow templates use placeholders instead of hard-coded local filenames. Download weights only from a trusted model publisher or a quantizer whose provenance you have reviewed. Verify file hashes when publishers provide them.

## Included templates

| Template | Additional requirement | Intended role |
|---|---|---|
| `qwen-image-edit-lightning-api.json` | Qwen edit model, Qwen VL encoder, VAE, Lightning LoRA | Native fidelity-first route |
| `nunchaku-qwen-image-edit-api.json` | ComfyUI-nunchaku and compatible Nunchaku wheel/model | Highest-quality accepted final |
| `flux2-klein-4b-edit-api.json` | FLUX.2 Klein model, Qwen 3 text encoder, FLUX.2 VAE | Fast aesthetic/preview route |

These are ComfyUI **API-format** graphs with `{{PLACEHOLDERS}}`; they are not UI-format workflow exports.

## Run a template

Start ComfyUI with its API reachable on the local machine, commonly `http://127.0.0.1:8188`.

```powershell
python scripts/run_workflow.py `
  --template workflows/qwen-image-edit-lightning-api.json `
  --image path/to/source.jpg `
  --prompt "Keep the exact product unchanged. Place it on a clean studio surface." `
  --set DIFFUSION_MODEL=qwen_image_edit_2511_fp8mixed.safetensors `
  --set TEXT_ENCODER=qwen_2.5_vl_7b_fp8_scaled.safetensors `
  --set VAE_MODEL=qwen_image_vae.safetensors `
  --set LORA_NAME=Qwen-Image-Lightning-2steps.safetensors `
  --set LORA_STRENGTH=1 `
  --set STEPS=2 `
  --set CFG=1 `
  --set DENOISE=0.85 `
  --set SEED=42 `
  --set OUTPUT_PREFIX=local-lab/qwen
```

Filenames are examples. Use names that match the files installed in your ComfyUI model directories and the recommendations on the relevant model card.

## Benchmark procedure

1. Restart ComfyUI for a true cold run.
2. Run the workflow once and record the end-to-end time.
3. Repeat at least three times without changing parameters.
4. Change the prompt while keeping the graph constant and repeat.
5. Inspect every output at native resolution.
6. Record peak VRAM and utilization separately from latency.
7. Save the prompt JSON embedded in the output PNG when available.
8. Report errors and rejected images, not only successful samples.

## Known compatibility risks

- Nunchaku wheels are tied to Python, PyTorch, CUDA, and GPU architecture combinations.
- An official ComfyUI update can change node inputs or model loading behavior.
- GGUF custom nodes and community quantizations may lag new model revisions.
- Blackwell FP4 files are not interchangeable with INT4 files intended for earlier GPUs.
- Model and adapter pairings may require a specific base revision.

Create a separate environment or ComfyUI installation for experimental custom nodes when stability matters.

## Publishing a result

Include the machine record, workflow template commit, replacements, prompt, seed, source hash, output, and timing class. A screenshot of a stopwatch is not enough to make a benchmark reproducible.
