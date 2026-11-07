# Install

1. Install [uv](https://docs.astral.sh/uv/) and Python 3.13.
2. Install [Git LFS](https://git-lfs.com/): the images are stored in it.
3. Clone this repository and run `uv sync --frozen` at its root.

On Windows the pinned `torch` is the CPU build. On Linux the same `uv.lock` brings the CUDA build and its libraries, which this project does not use.

The first `.\recipe.ps1 run` downloads the model, about 110 MB, into the HuggingFace cache, so it needs a network connection. Later runs read the cache. The weights are not in this repository and git never sees them.

`.\recipe.ps1 test` needs neither the weights nor a connection to the hub.

`.\recipe.ps1 build` packs the package into a wheel in `dist\`. Installed that way it runs as `swin-classify`.
