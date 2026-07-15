# References

Primary and upstream sources used to verify hardware specifications, software support, model capabilities, and licenses. Accessed July 15, 2026.

## Hardware

### NVIDIA

- [GeForce RTX 5060 family specifications](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5060-family/) - 5060 Ti VRAM options, CUDA cores, AI TOPS, and board power.
- [NVIDIA Blackwell GeForce RTX 5060 announcement](https://nvidianews.nvidia.com/news/nvidia-blackwell-geforce-rtx-arrives-for-every-gamer-starting-at-299) - $429 launch price for the 16 GB RTX 5060 Ti.
- [GeForce RTX 5070 family specifications](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5070-family/) - VRAM, CUDA cores, AI TOPS, and board power.
- [GeForce RTX 5080 specifications](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5080/) - VRAM, CUDA cores, AI TOPS, and board power.
- [RTX 50-series announcement](https://nvidianews.nvidia.com/news/nvidia-blackwell-geforce-rtx-50-series-opens-new-world-of-ai-computer-graphics) - RTX 5070/5070 Ti/5080 launch pricing and Blackwell FP4 positioning.
- [RTX 30-series introduction](https://www.nvidia.com/en-us/geforce/news/introducing-rtx-30-series-graphics-cards/) - RTX 3090 24 GB specification and launch price.
- [PNY RTX 5060 Ti 16 GB product listing](https://www.newegg.com/pny-technologies-inc-rtx-5060-ti-16gb-dual-fan-oc-geforce-rtx-5060-ti-graphics-card-double-fans/p/N82E16814985024?item=N82E16814985024) - exact board purchased for the experiment. The $530 refurbished purchase price is the author's transaction price, not a current-price claim.

### AMD

- [Radeon RX 9060 XT announcement](https://www.amd.com/en/newsroom/press-releases/2025-5-20-amd-introduces-new-radeon-graphics-cards-and-ryzen.html) - 16 GB option and $349 suggested e-tail price.
- [Radeon RX 9060 XT specifications](https://www.amd.com/en/products/graphics/desktops/radeon/9000-series/amd-radeon-rx-9060xt.html) - memory, bandwidth, and board power.
- [Radeon RX 9070 series announcement](https://www.amd.com/en/newsroom/press-releases/2025-2-28-amd-unveils-next-generation-amd-rdna-4-architectu.html) - RX 9070 and 9070 XT pricing and specifications.
- [ROCm on Radeon/Ryzen Windows compatibility](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/windows/windows_compatibility.html) - current Windows support scope and limitations.

### Intel

- [Intel Arc B580 specifications](https://www.intel.com/content/www/us/en/products/sku/241598/intel-arc-b580-graphics/specifications.html) - 12 GB memory and board power.
- [Intel Arc B-series launch](https://newsroom.intel.com/artificial-intelligence/intel-launches-arc-b-series-graphics-cards) - $249 recommended customer price.

## Runtime and workflow tools

- [ComfyUI system requirements](https://docs.comfy.org/installation/system_requirements) - supported operating systems, GPU backends, Python, and PyTorch guidance.
- [ComfyUI Windows desktop guidance](https://docs.comfy.org/installation/desktop/windows) - NVIDIA/CUDA scope of the Windows desktop distribution.
- [ComfyUI source](https://github.com/comfyanonymous/ComfyUI) - graph runtime and API server.
- [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) - GGUF model-loading custom nodes used in several experiments.
- [ComfyUI-nunchaku](https://github.com/nunchaku-ai/ComfyUI-nunchaku) - Nunchaku custom nodes and example workflows.
- [Nunchaku/SVDQuant](https://github.com/nunchaku-ai/nunchaku) - low-bit diffusion inference engine.

## Models and adapters

- [Qwen Image Edit 2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) - official model card, capabilities, Diffusers example, and Apache 2.0 license.
- [Qwen Image Edit 2511 Lightning](https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning) - distilled LoRA and fused FP8 variants.
- [Nunchaku Qwen Image Edit](https://huggingface.co/nunchaku-ai/nunchaku-qwen-image-edit) - official Nunchaku quantization guidance, including INT4 for pre-Blackwell and NVFP4 for Blackwell.
- [QuantFunc Nunchaku Qwen Image Edit 2511](https://huggingface.co/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511) - community quantization used for the tested 2511 ultimate-speed/balanced FP4 files. This is not an official Nunchaku release.
- [FLUX.2 Klein 4B](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B) - official model card, 4B architecture, image-editing support, VRAM guidance, limitations, and Apache 2.0 license.
- [FLUX.2 Klein 4B FP8](https://huggingface.co/black-forest-labs/FLUX.2-klein-4b-fp8) - official single-file FP8 model.
- [LongCat Image Edit Turbo](https://huggingface.co/meituan-longcat/LongCat-Image-Edit-Turbo) - official model card, eight-NFE distilled model, and Apache 2.0 license.
- [FireRed Image Edit 1.1](https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1) - official image-editing model card, quantization/distillation claims, and Apache 2.0 license.
- [Z-Image Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) - official 6B distilled model card and 16 GB consumer-device positioning.

## Reading these sources

Upstream latency claims often use datacenter GPUs, isolated model inference, fixed prompts, or optimized frameworks. They are not directly comparable to this repository's end-to-end Windows/ComfyUI measurements. Model cards also describe model-family capabilities, not a guarantee that every quantization or custom-node implementation preserves them.

Review each license at the exact model revision you download. A base model, adapter, quantization, custom node, and generated asset can have different terms.
