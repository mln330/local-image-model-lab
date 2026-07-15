# Hardware selection

## The machine and the purchase

The experiment workstation uses a **PNY Dual Fan OC GeForce RTX 5060 Ti 16 GB GDDR7** purchased refurbished for **$530** from [Newegg](https://www.newegg.com/pny-technologies-inc-rtx-5060-ti-16gb-dual-fan-oc-geforce-rtx-5060-ti-graphics-card-double-fans/p/N82E16814985024?item=N82E16814985024).

The purchase goal was broader than image generation. The card needed to support:

- current image-generation and image-editing models;
- local text and multimodal LLMs;
- coding assistants and agent experiments;
- speech recognition and synthesis;
- embeddings, retrieval, and evaluation workloads;
- Windows tools with a mature acceleration path;
- future experiments that were not known at purchase time.

The priorities were:

1. enough VRAM to avoid immediately limiting every experiment;
2. mature CUDA, PyTorch, and ComfyUI support;
3. useful low-precision support;
4. affordable entry cost;
5. moderate power and desktop practicality.

## Why 8 GB was too small

Eight gigabytes can run useful models. It would not support the range of work intended here without frequent compromises:

- more aggressive quantization;
- smaller context windows for LLMs;
- CPU offload and transfer stalls;
- lower image resolution;
- fewer resident components;
- older or smaller model families;
- less room for multimodal encoders and adapters.

The problem is not whether a graph can be forced to run. It is whether the graph is pleasant enough to evaluate and integrate.

## Why 12 GB was the minimum

Twelve gigabytes looked like the minimum useful tier. It offers significantly more freedom than 8 GB and can run strong 9B- to 12B-class LLM quantizations. It is still tight for the image graphs tested here.

The RTX 5070 illustrates the trade: it offers more raw compute than the 5060 Ti but only 12 GB. For a memory-bound local-AI workload, paying more to reduce capacity was not attractive.

## Why 16 GB was the right deal

Sixteen gigabytes did not make memory irrelevant. It made the interesting experiments possible:

- FLUX.2 Klein 4B FP8 and NVFP4 routes fit and ran quickly;
- native Qwen Image Edit could run through dynamic model management;
- a 12B LLM at a useful 4-bit or 5-bit quantization had room for context and runtime overhead;
- larger multimodal and MoE experiments became possible with careful quantization;
- model comparison did not begin from the smallest available option.

The 16 GB refurbished card was therefore a capacity purchase first and a gaming-tier purchase second.

## Current price snapshot

These are ordinary U.S. prices observed on **July 15, 2026**. They are a dated shopping snapshot, not a forecast. The bands exclude isolated in-store clearance prices and extreme third-party marketplace listings.

| GPU | VRAM | Board power | Launch/SEP | Observed July 2026 band | Local-AI assessment |
|---|---:|---:|---:|---:|---|
| RTX 5060 Ti 8 GB | 8 GB | 180 W | $379 | $360-$395 | Compute is affordable; capacity is too restrictive for this experiment mix |
| RTX 5060 Ti 16 GB | 16 GB | 180 W | $429 | $565-$570 | Best affordable CUDA capacity tier in this comparison; the test card was $530 refurbished |
| RTX 5070 | 12 GB | 250 W | $549 | $550-$670 | Faster compute but less memory, which makes the primary constraint worse |
| RTX 5070 Ti | 16 GB | 300 W | $749 | $900-$1,100 | Faster at the same capacity, with much higher acquisition cost |
| RTX 5080 | 16 GB | 360 W | $999 | $1,250-$1,600 | Substantially faster but still capped at 16 GB |
| Used RTX 3090 | 24 GB | 350 W | $1,499 | $1,189-$1,292 fair asking | Excellent headroom; high power, age, used risk, and unusually volatile pricing |
| RX 9060 XT 16 GB | 16 GB | 160 W | $349 | $400-$460 | Excellent capacity value if the exact backend and node graph are validated |
| RX 9070 XT | 16 GB | 304 W | $599 | $690-$850 | Strong performance/value with more software validation required for this Windows stack |
| Intel Arc B580 | 12 GB | 190 W | $249 | $300-$310 | Attractive entry cost, less headroom, and narrower tested custom-node support |

The observed bands use a multi-retailer price tracker for the 5060 Ti, Best Buy listings for the 5070 family, Newegg listings for the 5080 and AMD/Intel cards, and a 301-listing used-market sample for the 3090. Source links and caveats are in [References](references.md).

## Why image models consume more than their headline size

The tested graphs included combinations of:

- a diffusion transformer;
- a Qwen vision-language text encoder;
- a VAE;
- a Lightning LoRA;
- source-image latents;
- attention and sampling buffers;
- custom runtime allocations;
- output decode and save operations.

The native Qwen transformer was roughly 19 GB in its distributed mixed-FP8 form, and its vision-language encoder was another substantial component. ComfyUI made the graph run through dynamic loading and offload. That is not the same as keeping the complete graph resident.

Observed consequences:

- VRAM peaked near 15.3 GB in one monitored native Qwen run.
- Average GPU utilization was about 47%, with a 99% peak.
- Prompt changes could trigger text-encoding work and model transfers.
- Repeated prompts could appear faster because conditioning was reused.
- `--highvram` was counterproductive for the Qwen graph and caused it to hang.
- Switching between Qwen and FLUX created large cold-transition penalties.

This is why a 4B image model does not imply a 4B-sized application.

## Broader local-LLM implications

[Gemma 4 12B](https://huggingface.co/google/gemma-4-12B) is approximately 24 GB in BF16. Four-bit weights reduce the raw storage to roughly 6 GB before quantization metadata and runtime allocations, but the context cache, multimodal data, and serving framework still consume VRAM. An 8 GB card can make it run only with tight tradeoffs. Twelve gigabytes is a practical minimum; 16 GB leaves useful breathing room.

[Qwen3.6](https://huggingface.co/collections/Qwen/qwen36) currently includes a 27B dense model and a 35B-A3B MoE model. The MoE activates fewer parameters per token, but total weight storage and KV cache still matter. A 16 GB card requires a low-bit quantization, and context length must be chosen for available memory rather than copied from the maximum model specification.

The card can also host smaller models alongside applications, embeddings, speech pipelines, and development tools without treating every megabyte as an emergency. That flexibility was part of the purchase value.

## NVIDIA, AMD, and Intel

The hardware-only answer and the system answer differ.

AMD's 16 GB cards offer compelling dollars per gigabyte. Intel's B580 offers 12 GB at an accessible price. For a Linux-first project with time to validate backends, both deserve investigation.

This experiment used Windows, ComfyUI Desktop, PyTorch, CUDA-oriented model releases, and custom nodes. NVIDIA provided the shortest path from model card to working graph. That ecosystem advantage was worth money here, even though it does not make NVIDIA the universal value winner.

## Conclusion

The RTX 5060 Ti 16 GB was the best low-friction, capacity-first option available for this project at the time of purchase. The result should not be generalized into "the best AI GPU."

The lasting purchasing rule is more useful:

1. choose the workloads and model families first;
2. total the whole graph, not only the largest checkpoint;
3. treat VRAM as the first hard constraint;
4. price the software ecosystem and your validation time;
5. buy enough capacity for the experiments you have not planned yet.
