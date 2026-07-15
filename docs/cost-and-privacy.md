# Cost and privacy

Local image inference is not free. It replaces per-call pricing with hardware, electricity, maintenance, storage, and engineering time. The trade becomes attractive when generation volume, repeated experimentation, privacy, offline operation, or multi-workload use matters.

## Cloud price snapshot

Prices below were checked on **July 15, 2026**. They are examples, not a permanent market average.

| Service | Example image price | Notes |
|---|---:|---|
| FLUX.2 Klein 4B API | from $0.014 | Image editing and text-to-image; price scales with megapixels |
| Gemini 3.1 Flash Lite Image | $0.0336 at 1K | Cost-focused image generation/editing |
| Gemini 3.1 Flash Image | $0.067 at 1K; $0.151 at 4K | Higher-throughput general image route |
| Gemini 3 Pro Image | $0.134 at 1K/2K; $0.24 at 4K | Higher-quality route |
| GPT Image 1 | $0.042 medium 1K square | Input-image and prompt tokens are additional |
| GPT Image 1 | $0.167 high 1K square; $0.25 high portrait | Higher quality and larger outputs cost more |

Use the provider's live pricing page before making a purchasing or architecture decision. Models and prices change quickly.

## Local electricity estimate

Use:

```text
energy_kwh = system_watts / 1000 * seconds / 3600
electricity_cost = energy_kwh * price_per_kwh
```

For a deliberately conservative example:

- whole-system draw: 250 W;
- generation time: 8.4 seconds;
- electricity: 18.27 cents/kWh, the EIA's 2026 U.S. summer residential estimate.

```text
0.250 kW * 8.4 / 3600 = 0.000583 kWh
0.000583 * $0.1827 = $0.000107
```

The electricity is about one-hundredth of a cent per image. Model loading, idle time, retries, cooling, and storage add overhead, but hardware amortization dominates this calculation.

## Simple hardware break-even

Ignoring resale value, engineering time, and the GPU's other uses:

```text
break_even_images = hardware_cost / (cloud_cost - local_electricity_cost)
```

For a $530 GPU and $0.000107 local electricity:

| Avoided cloud price | Approximate break-even |
|---:|---:|
| $0.014 | 38,150 images |
| $0.0336 | 15,821 images |
| $0.067 | 7,924 images |
| $0.134 | 3,959 images |
| $0.167 | 3,176 images |
| $0.250 | 2,121 images |

The real unit of work is often a candidate, not a published image. A ten-image gallery with four candidates per asset and three prompt rounds can consume 120 generations. At that rate, 50 products represent 6,000 calls.

## Costs the simple table omits

Local costs:

- GPU and the rest of the workstation;
- electricity while loading, idling, and retrying;
- SSD capacity for model weights and outputs;
- setup, updates, driver changes, and custom-node compatibility;
- monitoring and failure recovery;
- time spent evaluating weaker local outputs;
- secure backups and access controls.

Cloud costs:

- generated output plus input-image and prompt tokens where applicable;
- failed or rejected candidates that are still billable;
- high-resolution and premium-quality multipliers;
- network latency and service limits;
- integration and provider-switching work;
- privacy review, data residency, and retention requirements.

Cloud is usually the rational choice for low volume, immediate access, burst scaling, and minimal maintenance. Local improves with steady volume, iterative evaluation, offline use, and a GPU shared across several AI workloads.

## Privacy boundary

Local execution can keep family photos, home interiors, prototypes, client assets, and unreleased designs off third-party services. That benefit is real only if the rest of the system respects the boundary.

Minimum controls:

- authenticate access to the local worker;
- bind ComfyUI or the worker API to a trusted interface;
- isolate uploaded sources and generated outputs by user or job;
- encrypt storage and backups;
- define deletion and retention policies;
- avoid logging full prompts, source paths, or image bytes;
- review custom nodes before installing or updating them;
- pin model and node revisions for repeatability;
- record provenance without recording private content;
- require explicit approval before any cloud fallback.

The private-cleanup example in this repository intentionally publishes only the approved output. The source remained local and is not part of the repository.

## Hybrid policy

A practical service can use local first and cloud by exception:

1. route supported, privacy-sensitive, and high-volume jobs locally;
2. reject or queue when the local worker lacks memory or a required model;
3. ask for explicit policy approval before sending a source to a cloud provider;
4. enforce per-job cloud budgets and maximum candidate counts;
5. record which provider processed each output;
6. compare local acceptance rate and total cost, not only nominal cost per call.

The purpose of local inference is not to declare the cloud bad. It is to make cost and data placement an architectural choice.
