# Local image model use cases

Local image generation is most compelling when privacy, iteration volume, offline use, or integration control matters. Product photography is one demanding example, not the limit of the hardware.

## Private photo cleanup

Family photos, home interiors, IDs visible in the background, client assets, and unreleased prototypes may not belong in a third-party service.

![A locally cleaned photograph of a 3D-printed planter and plant on a simple shelf](../assets/results/qwen-private-photo-cleanup.png)

The source for this example included a television and personal room context. It was processed locally and is intentionally not published. Only the approved output is in the repository.

Possible tasks:

- remove clutter or accidental background content;
- relight a dim room;
- replace a distracting background;
- repair a crop or extend the canvas;
- restore a scan;
- explore a style before committing to a destructive edit.

Local processing reduces data exposure. It does not replace authentication, encrypted storage, deletion policies, safe logs, or custom-node review.

## Game assets and visual prototyping

A reference photo can seed a game prop, inventory icon, storyboard element, or art-direction study.

![A rocket organizer transformed into an isometric game-prop concept](../assets/results/flux2-klein-game-asset.png)

Useful workflows:

- convert a physical prototype into a stylized concept;
- explore shape and palette families;
- create storyboard frames from rough references;
- generate placeholder props before final modeling;
- communicate a visual direction to artists and developers.

Generated concepts are not production geometry. They are fast decision artifacts.

## Synthetic data and evaluation fixtures

Image-editing models can create controlled viewpoint, background, weather, and lighting variants for computer-vision development.

![A neutral-background inspection variant of a rocket-shaped organizer](../assets/results/flux2-klein-synthetic-data.png)

Potential uses:

- bootstrap object-detection examples;
- create difficult lighting and partial-occlusion cases;
- test background sensitivity;
- generate UI fixtures for upload and moderation flows;
- build visual-regression sets without exposing real customer images.

Synthetic data can reproduce model bias and introduce identity drift. It should be labeled, reviewed, and kept separate from real holdout evaluation data.

## Confidential design iteration

Local models can support work that is valuable before it is public:

- client packaging and campaign mockups;
- industrial design and 3D-print concepts;
- interior and architectural studies;
- unreleased product colorways;
- private brand exploration;
- internal presentation art.

The local worker can remain inside a trusted network. A cloud provider can still be an explicit, approved fallback for requests the local stack cannot satisfy.

## Product and catalog photography

The original stress test remains broadly useful:

- turn an ordinary phone photo into a clean hero;
- replace a granite counter or fabric sweep with a plausible scene;
- create lifestyle, detail, scale, and gift-context candidates;
- test several art directions before staging a physical shoot;
- reduce repeated lighting and product-placement work.

The model must not silently redesign what a buyer will receive. Source identity is a business rule, not a visual preference.

## Restoration and archival work

Local processing is useful for sensitive family, institutional, or client archives:

- dust and scratch cleanup;
- gentle color restoration;
- denoise and relighting;
- crop repair;
- alternate restoration candidates for human review.

Preserve the original file, record every transformation, and do not present a generated reconstruction as historical fact.

## Diagrams and presentation visuals

An image model can create:

- an unlabeled architecture illustration;
- background scenes and textures;
- conceptual cutaways;
- visual metaphors;
- icons or art-direction references.

It should not be the authority for factual labels, dimensions, values, or citations. Generate the visual layer locally, then render text, arrows, legends, and measurements with deterministic code.

## Offline creative tools

A local model can power:

- a desktop batch editor;
- an internal asset workstation;
- an offline field tool;
- a private photo kiosk;
- a creative coding environment;
- an automation pipeline without external rate limits.

The application should call a versioned worker API rather than depending directly on raw ComfyUI node IDs. The worker can advertise models, free VRAM, maximum resolution, and supported intents.

## High-volume evaluation and learning

Once the hardware and weights are available, another prompt or seed has almost no marginal API cost. This is useful for:

- prompt-ablation studies;
- quantization comparisons;
- seed sensitivity tests;
- evaluation-set generation;
- workflow regression tests;
- model-upgrade acceptance tests;
- teaching and experimentation.

Local generation does not make brute force automatically wise. It makes broad evaluation economically possible.

## Choosing local, cloud, or hybrid

Use local first when:

- source privacy matters;
- the workload is steady or iterative;
- the model and graph fit the available hardware;
- offline operation is valuable;
- workflow control and provenance matter.

Use cloud first when:

- volume is low or highly bursty;
- the best proprietary quality is required;
- there is no appetite for runtime maintenance;
- the local graph repeatedly fails validation;
- a large model or resolution exceeds local capacity.

Use a hybrid policy when privacy, cost, and quality differ by request. Make the routing decision visible and auditable.
