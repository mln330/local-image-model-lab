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
| `flux2-klein-4b-edit-api.json` | FLUX.2 Klein model, Qwen 3 text encoder, FLUX.2 VAE | Practical text-free scene route and fast preview |

These are ComfyUI **API-format** graphs with `{{PLACEHOLDERS}}`; they are not UI-format workflow exports.

## Run a template

Start ComfyUI with its API reachable on the local machine, commonly `http://127.0.0.1:8188`. ComfyUI Desktop may select a different port; pass it through `--server`.

```powershell
python scripts/run_workflow.py `
  --server http://127.0.0.1:8000 `
  --template workflows/flux2-klein-4b-edit-api.json `
  --image path/to/source.jpg `
  --prompt "Preserve the exact object and place it naturally on a bright desk. No text." `
  --set DIFFUSION_MODEL=flux-2-klein-4b-fp8.safetensors `
  --set TEXT_ENCODER=qwen_3_4b_fp4_flux2.safetensors `
  --set VAE_MODEL=flux2-vae.safetensors `
  --set MEGAPIXELS=0.8 `
  --set STEPS=6 `
  --set CFG=1 `
  --set SEED=42 `
  --set OUTPUT_PREFIX=local-lab/flux
```

Filenames are examples. Use names that match the files installed in your ComfyUI model directories and the recommendations on the relevant model card.

## Benchmark procedure

1. Restart ComfyUI for a true cold run.
2. Run the workflow once and record the end-to-end time.
3. Repeat at least three times without changing parameters.
4. Change the prompt while keeping the graph constant and repeat.
5. Change the source image while keeping the graph constant and repeat.
6. Inspect every output at native resolution.
7. Record peak VRAM and utilization separately from latency.
8. Save the prompt JSON embedded in the output PNG when available.
9. Report errors and rejected images, not only successful samples.

Do not average a model-family transition into warm latency. Report cold process start, cold route switch, warm varied prompt, and warm repeated prompt separately.

## Known compatibility risks

- An official ComfyUI update can change node inputs or model loading behavior.
- GGUF custom nodes and community quantizations may lag new model revisions.
- Blackwell FP4 files are not interchangeable with INT4 files intended for earlier GPUs.
- Model and adapter pairings may require a specific base revision.

Create a separate environment or ComfyUI installation for experimental custom nodes when stability matters.

## Publishing a result

Include the machine record, workflow template commit, replacements, prompt, seed, source hash, output, and timing class. A screenshot of a stopwatch is not enough to make a benchmark reproducible.
