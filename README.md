# HyperShot

A Codex skill for careful tiled generative image restoration and print preparation. It is an agent workflow, not a self-contained image-generation model: an image-editing model/tool is required for the enhancement step. The included Python helper splits images and assembles aligned tiles; it does not generate detail or guarantee seamless results.

## Install

In Codex, ask: `Install the hypershot skill from https://github.com/siroj30/HyperShot, path hypershot`. Restart Codex if needed, then invoke `$hypershot` and supply an image, target print size and any character references. Support for skill installation and image editing depends on your agent environment.

## Helper

Install Python 3.10+ and Pillow (`python -m pip install Pillow`).

```
python hypershot/scripts/tiles.py split input.png work --rows 2 --cols 2 --overlap 0.25
# Edit work/input-tiles/tile-*.png using your image-editing tool, save the
# corresponding results under work/edited with the exact same file names.
python hypershot/scripts/tiles.py assemble work/input-tiles/manifest.json work/edited output.png --scale 2 --dpi 300
```

Inspect the result thoroughly: independently generated tiles can shift objects and produce seams or inaccurate identities. The helper does not perform content-aware registration. 300 dpi metadata does not create detail; calculate effective ppi using the final pixel dimensions and physical print size. Never submit generated inscriptions or reconstructed historical patterns as verified source text.

The skill does not include image models, proprietary project assets, credentials, or API access.
