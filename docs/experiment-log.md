# Experiment log

This log records the progression of the research rather than only the final winners. Timings are warm end-to-end observations unless marked cold.

## 1. Segmentation and generated backgrounds

The first pipeline isolated the product, generated a separate background, and composited the cutout into it.

**What worked:** deterministic preservation of the source pixels, reusable masks, controllable layout.

**What failed:** scene integration. Lighting, contact shadow, perspective, and scale did not naturally agree. A generic shadow pass could make the composite less obvious but did not make the product belong to the scene.

**Decision:** keep segmentation for validation, masks, and deterministic layouts; use an instruction-based image editor for premium lifestyle scenes.

## 2. Native Qwen Image Edit 2511

### Full-quality baseline

- approximately 40 steps;
- roughly six minutes per image;
- excellent identity and text preservation.

**Decision:** quality proof, latency rejection.

### Lightning, two steps

- 768-class output;
- approximately 11-12 seconds warm;
- strong preservation and useful scene changes.

**Decision:** accepted as the quality favorite and general fidelity-first default.

In the final system assessment this became the **quality favorite**. It was faster than the tested Nunchaku route and required a more conventional native graph.

### Lightning, three steps

- approximately 22-26 seconds warm;
- stronger polish than two steps;
- still inside the 30-second final target.

**Decision:** optional higher-polish native Qwen route.

### Lightning, one step

- approximately 8-14 seconds;
- smeary details and unreliable product lettering.

**Decision:** rejected. It saved seconds by crossing the quality boundary.

### 640-class two-step route

- as low as approximately seven seconds with a repeated/cached prompt;
- approximately 12 seconds with varied listing prompts;
- good product fidelity at lower native detail.

**Decision:** accepted as `Base`; do not describe the cached seven-second figure as normal varied-prompt latency.

### Memory behavior

- monitored GPU utilization averaged approximately 47% and peaked at 99%;
- VRAM peaked near 15.3 GB;
- forcing `--highvram` hung the graph.

**Decision:** retain normal dynamic model management. Optimize end-to-end flow instead of forcing residency that does not fit.

## 3. FLUX Kontext

- eight to 12 steps;
- approximately 21-32 seconds;
- good edits, but no consistent quality advantage over the faster Qwen route.

**Decision:** viable, not selected.

## 4. Qwen GGUF

### Q2_K

- 640x480, two steps;
- approximately 30 seconds cold;
- approximately 14-15 seconds warm.

### Q3_K_M

- approximately 28 seconds cold;
- approximately 18-19 seconds warm;
- slightly stronger quality than Q2.

**Decision:** both fit and work, but neither beats native Qwen Lightning on the tested machine. Quantization solved capacity more than latency.

## 5. QuantFunc Qwen 2511 through Nunchaku

The `ultimate_speed` and `balance` FP4 checkpoints in this section are community quantizations published by QuantFunc and executed through the Nunchaku runtime. They are not official Nunchaku releases.

### Ultimate-speed FP4, 0.5 MP

- approximately 23-24 seconds warm with varied prompts;
- strong text and identity preservation.

### Ultimate-speed FP4, 0.8 MP

- approximately 25-27 seconds warm with varied prompts;
- best complete balance of identity, scene integration, and listing appeal.

**Decision:** excellent individual result, but not selected for the operating stack. The route was slower than native Qwen Lightning and added custom-runtime and checkpoint-provenance overhead.

### Balanced FP4, 0.8 MP

- approximately 67 seconds warm;
- only a modest visible quality improvement.

**Decision:** rejected for interactive/customer use.

### Why Nunchaku was not faster than native Lightning

The FP4 diffusion model is only one part of the graph. The Qwen vision-language text encoder, VAE, LoRA stack, model transitions, custom-node implementation, and larger output target still contribute. "Ultimate speed" is a model variant, not an end-to-end service-level guarantee.

The important correction is that image quality, latency, and operability must be evaluated separately. Nunchaku won one inspected output comparison. It did not win the system decision.

## 6. FLUX.2 Klein 4B

### Distilled FP8, 0.8 MP, six steps

- approximately seven seconds warm;
- excellent scene composition and aesthetics;
- changed the personalized text and several artwork details in the inspected lifestyle result.

**Decision:** accepted as the practical default for fast scene generation when the new scene does not require exact generated text. Validate existing product text and intricate artwork before publication.

### NVFP4, 0.8 MP, four steps

- approximately four to five seconds warm;
- fastest accepted preview route;
- visible identity risk.

**Decision:** accepted as the fastest interactive preview and candidate-generation route.

### NVFP4, 1.2 MP, four steps

- approximately six to seven seconds warm;
- larger output with similar routing caveat.

**Decision:** accepted as the larger interactive route.

### NVFP4, approximately 2 MP, six steps

- approximately 17 seconds warm.

**Decision:** too slow to justify as the default preview when the output still required fidelity validation.

### Base FP8, 12-24 steps

- approximately 12-23 seconds;
- repeatedly rewrote product artwork and text.

**Decision:** rejected for source-contract work.

### July 15 follow-up with a second owned product

The original FLUX interpretation leaned too heavily on one personalized sign. A follow-up used an owned 3D-printed rocket-shaped pen organizer with no source lettering and an ordinary fabric-background source photo.

- FP8 distilled, 0.8 MP, six steps;
- varied lifestyle prompt;
- 8.4 seconds warm after the FLUX graph was resident;
- strong scene composition, believable contact, preserved print texture, and no text problem;
- a controlled synthetic-data variant completed in 7.6 seconds warm;
- a cold model-family transition took much longer and was not treated as warm latency.

**Decision:** the follow-up confirmed that FLUX.2 Klein was undersold by the text-heavy sign test. For text-free scene work it offered the best practical combination of speed, consistency, and aesthetics.

The follow-up also reran the native Qwen template after a ComfyUI Desktop and PyTorch update. Two diagnostic runs took approximately 156-166 seconds because the graph repeatedly loaded or offloaded major components. Those values are preserved in `data/followup-runs-2026-07-15.json` but are not substituted for the earlier controlled 11-12 second warm benchmark. They are evidence that runtime version and model-residency behavior must be pinned and regression-tested.

## 7. LongCat Image Edit Turbo

### Official BF16 Diffusers

- approximately 441 seconds to load;
- approximately 1,112 seconds to generate;
- good quality.

**Decision:** proof that the machine could run the route with offload, not a usable configuration.

### GGUF Q3/Q4/Q5 K_M

- approximately 41-43 seconds at guidance 1.0;
- solid identity preservation;
- guidance 4.5 produced blurry output.

**Decision:** research-capable but outside the 30-second target.

## 8. FireRed Image Edit 1.1

- Q3_K_M plus eight-step Lightning adapter;
- approximately 74 seconds;
- one of the strongest studio results, with excellent text/art preservation.

**Decision:** rejected on latency. Kept as evidence that quality alone is not the routing criterion.

## 9. Z-Image Turbo

- Q3_K_M image-to-image;
- eight steps, denoise 0.55;
- approximately 32 seconds;
- preserved the granite source setting and introduced conspicuous star artifacts.

**Decision:** rejected for this workflow and configuration.

## Final operating choices

| Decision | Configuration | Role |
|---|---|---|
| Practical default | FLUX.2 Klein distilled FP8, 0.8 MP, six steps | Fast, attractive text-free scene generation |
| Quality favorite | Native Qwen 2511 + Lightning, 768-class, two steps | Product identity, artwork, and existing text |
| Fast preview | FLUX.2 Klein NVFP4, 0.8 MP, four steps | Lowest-latency visual direction |
| Larger fast preview | FLUX.2 Klein NVFP4, 1.2 MP, four steps | Interactive candidate with more pixels |
| Lower-resolution fidelity route | Native Qwen 2511 + Lightning, 640-class, two steps | Fidelity-first preview when native detail can be lower |
| Tested, not selected | QuantFunc Qwen 2511 FP4 through Nunchaku, 0.8 MP | Strong output, but slower and operationally heavier |

These are workload roles on one workstation, not global rankings. The default route is chosen by scene text and identity risk, not by a universal tier label.
