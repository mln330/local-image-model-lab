# Prompt engineering for source-faithful image edits

Prompting was not a cosmetic layer on top of the model tests. It changed product fidelity, physical integration, composition, and failure rate enough to be part of the system design.

## The core prompt pattern

Use four ordered sections:

```text
[Intent]
Create a polished lifestyle photograph of the exact object in the reference.

[Preservation contract]
Preserve the cream body, red fins, black outlines, orange flame, circular
window, storage geometry, print-layer texture, and the same contents.

[Scene and physical integration]
Place it naturally on a bright homework desk. Use soft window light from the
left, a realistic contact shadow, coherent reflections, shallow depth of
field, and a natural three-quarter camera angle.

[Exclusions]
Do not add, remove, duplicate, resize, or redesign the object. No new text,
labels, badges, arrows, hands, people, or watermark.
```

The order is deliberate. Identity comes before styling. A prompt that begins with "make this creative" grants freedom before defining what must remain fixed.

## Write a ranked preservation contract

List five to eight traits that determine whether the output still depicts the source:

- silhouette and proportions;
- material and surface texture;
- dominant colors;
- functional geometry and openings;
- existing artwork, logo, or text;
- distinctive edges, fasteners, handles, or attachments;
- the number and arrangement of repeated elements;
- contents that must remain present.

Do not transcribe every visible pixel. A contract should tell the model what has business meaning. Long undifferentiated lists make priorities less clear.

## Ask for one asset intent

| Asset intent | Prompt emphasis | Common failure |
|---|---|---|
| Clean hero | Complete silhouette, sparse surface, controlled shadow | Props compete with the subject |
| Lifestyle | Plausible use context, camera, lighting, contact | Object looks pasted into the scene |
| Detail | Named material or feature, macro lens language | Model invents geometry outside the crop |
| Scale | Nearby familiar object, neutral perspective | Reference object is the wrong size |
| Gift context | Recipient/occasion cues without obscuring product | Hands or wrapping cover identity features |
| Cleanup | Explicit removal list and unchanged-subject contract | Model redesigns the subject while removing clutter |
| Concept asset | State which traits may change and which are inspiration | Output is mistaken for a faithful product edit |
| Controlled variant | Camera, light, background, and framing constraints | Synthetic drift contaminates an evaluation set |

Do not ask one prompt for "a complete listing gallery." Generate each asset type independently so it can be evaluated against its own rules.

## Describe why the object belongs in the scene

Useful scene language is concrete:

- "on a child-friendly homework desk" is better than "in a nice room";
- "soft morning window light from the left" is better than "professional lighting";
- "realistic contact shadow and coherent reflections" is better than "seamless";
- "natural three-quarter camera angle" is better than "dynamic angle";
- "calm uncluttered background" is better than a long list of decorative props.

Physical cues reduce the cutout-on-background effect. The model needs to solve support, light, shadow, and camera perspective together.

## Text policy

Separate three cases:

1. **Preserve existing source text.** Put the exact text in the preservation contract and route to native Qwen first.
2. **Invent new scene text.** Avoid it in FLUX-first scene workflows unless the output will be reviewed and repaired.
3. **Render factual labels, dimensions, prices, or legal text.** Generate the visual without them, then add them with deterministic code.

The dimension experiments produced attractive arrows with incorrect values. That is a hard boundary. Visual fluency is not factual reliability.

## Model-specific guidance

### FLUX.2 Klein

Use FLUX for text-free scene generation, art direction, and fast composition exploration.

- Keep the preservation list short and concrete.
- Explicitly say "no text, labels, badges, or arrows" when the scene does not need them.
- Specify light direction, contact, and camera angle.
- Prefer one believable environment over a dense prop list.
- Validate small geometry and source artwork even when the image looks excellent.

### Native Qwen Image Edit 2511

Use Qwen when source identity, artwork, or text matters most.

- Quote exact source lettering when it is business-critical.
- Name the geometry that may not move or disappear.
- Use denoise as a fidelity control, not only a creativity knob.
- Keep negative conditioning focused; a long negative prompt adds work and can muddy priorities.
- Two Lightning steps were the best warm speed/fidelity point in the tested configuration; three steps are an optional polish route.

## Prompt templates

### Clean hero

```text
Create a clean studio hero photograph of the exact [object] from the reference.
Preserve [five to eight identity traits]. Center the complete object on a
[surface] against a [background], with soft [light direction], a realistic
contact shadow, accurate material texture, and a [camera angle]. Keep generous
negative space and the complete silhouette visible. Do not add, remove,
duplicate, resize, or redesign the object. No new text, labels, badges, arrows,
hands, people, or watermark.
```

### Lifestyle

```text
Create a polished lifestyle photograph of the exact [object] from the
reference. Preserve [identity traits]. Place it naturally in [specific use
context] with [two restrained props]. Use [light direction and quality], a
realistic contact shadow, coherent reflections, shallow depth of field, and a
natural [camera angle]. Keep the object as the clear subject. Do not add,
remove, duplicate, resize, or redesign it. No new text, labels, badges, arrows,
hands, people, or watermark.
```

### Private photo cleanup

```text
Edit this private photo while preserving the exact [subject and dependent
elements]. Remove [specific distractions]. Place the unchanged subject on/in
[simple replacement context] with [light plan], realistic contact, and calm
neutral styling. No added people, logos, text, or decorative clutter.
```

### Concept or game asset

```text
Transform the [source object] into a [asset type]. Preserve the recognizable
[palette, motif, silhouette], but simplify it into [allowed style]. Show it at
a [camera angle] on a simple neutral background with a soft shadow and readable
silhouette. No text, interface frame, badge, people, watermark, or extra items.
```

### Synthetic-data variant

```text
Create a controlled synthetic-data photograph of the same exact [object].
Preserve [identity traits]. Show it from [viewpoint] on [neutral surface] under
[controlled lighting], with the complete silhouette visible and clean framing.
No other objects, text, labels, ruler, chart, hands, people, watermark, or UI.
```

## Evaluation loop

For each prompt revision:

1. lock the model graph, resolution, steps, denoise, and seed set;
2. change one prompt concept at a time;
3. compare source identity before judging aesthetics;
4. inspect contact edges, repeated geometry, text, hands, and reflections at full resolution;
5. record whether the prompt was repeated or varied because conditioning caches affect latency;
6. reject prompts that succeed only on one convenient seed;
7. save the prompt, graph version, model revision, seed, and output together.

## What did not work

- Broad requests such as "make a great listing image" gave the model too much freedom.
- Decorative prop lists made scenes busy and increased occlusion.
- Large negative prompts did not substitute for a clear positive preservation contract.
- Asking the model to render exact measurements produced plausible but incorrect facts.
- Repeating an identical prompt made some speed results look better than a real varied workload.
- Product-type flags were not a scalable solution. Structured source analysis and an asset-intent taxonomy generalized better.

The best prompt is not the most elaborate one. It is the shortest prompt that makes identity, scene intent, physical integration, and forbidden changes unambiguous.
