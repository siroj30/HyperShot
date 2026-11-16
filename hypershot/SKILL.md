---
name: hypershot
description: Restore and upscale illustrations or images for print using overlapping AI-enhanced tiles, careful identity and style preservation, and full-resolution quality checks.
---

# HyperShot

Use for deliberate, generative image restoration and print enlargement. This is a workflow for an agent with an image-editing model, not a standalone neural upscaler. Confirm the source and available character or object references. Preserve the original composition, framing, style, identities and expressions. Repair only visible defects and requested mismatches; never turn a painting into a photograph or invent legible text or historical patterns.

## Workflow

1. Inspect the original at full size, identify people, hands, text, ornament and contacts. Record source hash, pixel size, target physical dimensions and references. Determine needed pixels: millimeters / 25.4 × target ppi. DPI metadata alone adds no detail.
2. Split into overlapping crops with `scripts/tiles.py split`. Use 4–10 pieces: around 4 for half-page and up to 10 for detailed full-page art; use ample overlap and avoid placing seams through faces or writing where possible. Retain originals.
3. Use an available image-editing model on every crop with the source crop and relevant references. Ask it to preserve exact geometry, composition, identities, clothing, painted or photographic style, color and lighting. Repair only verified errors; preserve distinct people and avoid generic face enhancement. Save each result with the same tile name and original framing. Record the model and prompts.
4. Assemble using `scripts/tiles.py assemble` as a draft. The helper rescales and blends overlaps but does not register displaced content. Visually inspect every overlap at full resolution; if generated content drifted, use proper registration or redo tiles. Review people, hands, animals, physical contacts, text and ornaments against the source and references. Reject doubled edges, invented inscriptions, altered designs and style drift. Do not call a result perfect solely because scripts succeeded.
5. Export PNG with print-resolution metadata and inspect pixels against actual print dimensions. Record output hash, image size, effective ppi, edits and uncertainties. Never overwrite originals or publish without authorization.

Examples and installation: see the repository README. Project-specific APIs, credentials, catalogues and output locations must be supplied by the user; never hard-code or publish credentials or private assets.
