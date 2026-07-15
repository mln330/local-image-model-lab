# Hardware selection

## Decision

The experiment workstation uses a **PNY Dual Fan OC GeForce RTX 5060 Ti 16 GB GDDR7** purchased refurbished for **$530** from [Newegg](https://www.newegg.com/pny-technologies-inc-rtx-5060-ti-16gb-dual-fan-oc-geforce-rtx-5060-ti-graphics-card-double-fans/p/N82E16814985024?item=N82E16814985024).

The decision was based on workload fit, not a claim that the 5060 Ti is the best GPU for every local-AI user.

## Workload priorities

In order:

1. Enough VRAM for modern image-editing pipelines.
2. Reliable Windows support across CUDA, PyTorch, ComfyUI, and custom nodes.
3. Support for low-precision Blackwell paths such as NVFP4.
4. Acquisition cost appropriate for an enthusiast/developer workstation.
5. Power and cooling that do not require rebuilding the rest of the machine.
6. Throughput.

The ordering matters. Moving from a 16 GB 5060 Ti to a faster 12 GB 5070 would improve compute while making the primary constraint worse.

## Comparison at the time of publication

| GPU | VRAM | Memory | Board power | Official launch/SEP | Local-image assessment |
|---|---:|---|---:|---:|---|
| RTX 5060 Ti 16 GB | 16 GB | GDDR7 | 180 W | $429 | Best fit for this Windows/CUDA experiment; enough VRAM for the accepted quantized routes |
| RTX 5070 | 12 GB | GDDR7 | 250 W | $549 | Faster compute, but the 12 GB ceiling is a meaningful regression for these graphs |
| RTX 5070 Ti | 16 GB | GDDR7 | 300 W | $749 | Stronger version of the same basic capacity tier at higher cost and power |
| RTX 5080 | 16 GB | GDDR7 | 360 W | $999 | Much faster, but still 16 GB and outside the affordable-entry goal |
| RTX 3090 | 24 GB | GDDR6X | 350 W | $1,499 | Excellent capacity if a trustworthy used card and adequate PSU/cooling are available |
| Radeon RX 9060 XT 16 GB | 16 GB | GDDR6 | 160 W | $349 SEP | Outstanding paper value; exact Windows/custom-node compatibility needs verification |
| Radeon RX 9070 | 16 GB | GDDR6 | 220 W | $549 SEP | Attractive hardware, with more runtime friction for this CUDA-oriented test matrix |
| Radeon RX 9070 XT | 16 GB | GDDR6 | 304 W | $599 SEP | Strong compute/value; same software-stack caveat |
| Intel Arc B580 | 12 GB | GDDR6 | 190 W | $249 | Excellent entry price and improving XPU support, but less headroom and a narrower tested node ecosystem |

Prices are launch prices or suggested e-tail prices, not a statement about current street pricing. Used prices vary by market and condition.

## Why 16 GB was the floor

The native Qwen image transformer used in the tests is roughly 19 GB, while the vision-language text encoder is another large component. The complete graph also needs a VAE, adapters, intermediate tensors, and runtime overhead.

ComfyUI can make that graph run on 16 GB by dynamically loading and offloading components. That is very different from saying the complete graph fits comfortably in 16 GB.

Observed consequences:

- VRAM peaked around 15.3 GB in a monitored native Qwen run.
- Average GPU utilization was only about 47% even though it reached 99% during active kernels.
- Cold runs and prompt changes exposed model-transfer and text-encoding costs.
- `--highvram` was counterproductive and caused the Qwen graph to hang.
- Quantized models improved feasibility, but the text encoder and graph transitions remained significant.

A 24 GB card would reduce some of this pressure. A 12 GB card would increase it.

## Why not the used RTX 3090?

For a dedicated local-AI box, a good used 3090 remains one of the most interesting alternatives because 24 GB changes which models can remain resident.

The tradeoffs are not trivial:

- 350 W board power versus 180 W for the 5060 Ti;
- larger PSU and cooling requirements;
- variable card history and warranty;
- older architecture and no Blackwell-native FP4 path;
- used prices that can erase the apparent value advantage.

Someone comfortable buying used hardware and prioritizing model capacity over efficiency may reasonably choose the 3090 instead.

## Why not AMD or Intel?

This is a software-support decision, not a dismissal of the hardware.

ComfyUI supports manual installs across NVIDIA, AMD, and Intel hardware. Its Windows desktop and portable paths remain most straightforward on NVIDIA. AMD's Windows PyTorch/ROCm support now includes current Radeon generations, but AMD documents that the entire ROCm stack is not yet supported on Windows. Intel Arc has native `torch.xpu` support, but individual custom nodes and quantized kernels still need verification.

For a fresh Linux build, or for someone willing to validate each node, the RX 9060 XT 16 GB is particularly worthy of testing. For this Windows experiment, CUDA removed enough uncertainty to justify paying more.

## Purchase conclusion

The 5060 Ti 16 GB was the best **low-friction fit** I could acquire for the project. The phrase is intentionally narrower than "best value." Its most important properties were 16 GB of VRAM, Blackwell precision support, mature CUDA compatibility, and moderate power.

The $530 refurbished price should not be used as a market recommendation. It is the actual cost basis for the results in this repository.

See [References](references.md) for primary specification and runtime sources.
