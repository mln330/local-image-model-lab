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
- [RTX 3090 used-market snapshot](https://resaleprices.com/gpu/nvidia-rtx-3090) - July 14, 2026 fair asking range of $1,189-$1,292 from 301 listings.
- [PNY RTX 5060 Ti 16 GB product listing](https://www.newegg.com/pny-technologies-inc-rtx-5060-ti-16gb-dual-fan-oc-geforce-rtx-5060-ti-graphics-card-double-fans/p/N82E16814985024?item=N82E16814985024) - exact board purchased for the experiment. The $530 refurbished purchase price is the author's transaction price, not a current-price claim.
- [PC Gamer GPU price watch](https://www.pcgamer.com/hardware/graphics-cards/graphics-card-price-watch-deals/) - multi-retailer July 2026 spot prices for RTX 5060 Ti 8 GB and 16 GB cards.
- [Best Buy RTX 5070 and 5070 Ti listings](https://www.bestbuy.com/site/searchpage.jsp?browsedCategory=cat00000&id=pcat17071&qp=gpusv_facet%3DGraphics+Processing+Unit+%28GPU%29~NVIDIA+GeForce+RTX+5070%5Egpusv_facet%3DGraphics+Processing+Unit+%28GPU%29~NVIDIA+GeForce+RTX+5070+Ti&st=categoryid%24cat00000) - July 2026 retail examples used to form the observed bands.
- [Newegg RTX 5080 listings](https://www.newegg.com/p/pl?d=rtx+5080+16gb) - July 2026 retail examples; premium collector and marketplace outliers were excluded from the summary band.

### AMD

- [Radeon RX 9060 XT announcement](https://www.amd.com/en/newsroom/press-releases/2025-5-20-amd-introduces-new-radeon-graphics-cards-and-ryzen.html) - 16 GB option and $349 suggested e-tail price.
- [Radeon RX 9060 XT specifications](https://www.amd.com/en/products/graphics/desktops/radeon/9000-series/amd-radeon-rx-9060xt.html) - memory, bandwidth, and board power.
- [Radeon RX 9070 series announcement](https://www.amd.com/en/newsroom/press-releases/2025-2-28-amd-unveils-next-generation-amd-rdna-4-architectu.html) - RX 9070 and 9070 XT pricing and specifications.
- [Newegg RX 9070 XT listings](https://www.newegg.com/p/pl?d=rx+9070+xt+16gb) - July 2026 retail examples used for the observed price band.
- [Newegg Arc and RX 9060 XT listings](https://www.newegg.com/p/pl?d=arc+b580+gpu) - July 2026 retail examples for the Arc B580 and RX 9060 XT.
- [ROCm on Radeon/Ryzen Windows compatibility](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/windows/windows_compatibility.html) - current Windows support scope and limitations.

### Intel

- [Intel Arc B580 specifications](https://www.intel.com/content/www/us/en/products/sku/241598/intel-arc-b580-graphics/specifications.html) - 12 GB memory and board power.
- [Intel Arc B-series launch](https://newsroom.intel.com/artificial-intelligence/intel-launches-arc-b-series-graphics-cards) - $249 recommended customer price.

## Runtime and workflow tools

- [ComfyUI system requirements](https://docs.comfy.org/installation/system_requirements) - supported operating systems, GPU backends, Python, and PyTorch guidance.
- [ComfyUI Windows desktop guidance](https://docs.comfy.org/installation/desktop/windows) - NVIDIA/CUDA scope of the Windows desktop distribution.
- [ComfyUI source](https://github.com/comfyanonymous/ComfyUI) - graph runtime and API server.
- [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) - GGUF model-loading custom nodes used in several experiments.

## Models and adapters

- [Qwen Image Edit 2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) - official model card, capabilities, Diffusers example, and Apache 2.0 license.
- [Qwen Image Edit 2511 Lightning](https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning) - distilled LoRA and fused FP8 variants.
- [FLUX.2 Klein 4B](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B) - official model card, 4B architecture, image-editing support, VRAM guidance, limitations, and Apache 2.0 license.
- [FLUX.2 Klein 4B FP8](https://huggingface.co/black-forest-labs/FLUX.2-klein-4b-fp8) - official single-file FP8 model.
- [LongCat Image Edit Turbo](https://huggingface.co/meituan-longcat/LongCat-Image-Edit-Turbo) - official model card, eight-NFE distilled model, and Apache 2.0 license.
- [FireRed Image Edit 1.1](https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1) - official image-editing model card, quantization/distillation claims, and Apache 2.0 license.
- [Z-Image Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) - official 6B distilled model card and 16 GB consumer-device positioning.

## Broader local models

- [Gemma 4 12B](https://huggingface.co/google/gemma-4-12B) - official 12B unified multimodal model card and approximately 24 GB BF16 weight size.
- [Qwen3.6 collection](https://huggingface.co/collections/Qwen/qwen36) - official Qwen collection containing the 27B dense and 35B-A3B MoE variants.
- [Qwen3.6 27B model card](https://huggingface.co/Qwen/Qwen3.6-27B) - context, serving guidance, and memory-related recommendations.

## Cloud pricing and electricity

- [Black Forest Labs API pricing](https://docs.bfl.ai/quick_start/pricing) - FLUX.2 Klein, Pro, Max, and Flex per-image pricing accessed July 15, 2026.
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) - Gemini 3.1 Flash Image, Flash Lite Image, and Gemini 3 Pro Image output pricing accessed July 15, 2026.
- [OpenAI GPT Image 1 model pricing](https://developers.openai.com/api/docs/models/gpt-image-1) - per-image quality and size examples accessed July 15, 2026.
- [EIA 2026 summer residential electricity estimate](https://www.eia.gov/outlooks/steo/tables/pdf/sf02.pdf) - 18.27 cents/kWh U.S. summer estimate used in the local electricity example.

## Reading these sources

Upstream latency claims often use datacenter GPUs, isolated model inference, fixed prompts, or optimized frameworks. They are not directly comparable to this repository's end-to-end Windows/ComfyUI measurements. Model cards also describe model-family capabilities, not a guarantee that every quantization or custom-node implementation preserves them.

Review each license at the exact model revision you download. A base model, adapter, quantization, custom node, and generated asset can have different terms.
