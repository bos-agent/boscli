# boscli

[![Release to PyPI](https://github.com/bos-agent/boscli/actions/workflows/release.yml/badge.svg)](https://github.com/bos-agent/boscli/actions/workflows/release.yml)
[![Sync with bos-ai](https://github.com/bos-agent/boscli/actions/workflows/sync.yml/badge.svg)](https://github.com/bos-agent/boscli/actions/workflows/sync.yml)

A thin CLI shim package for [bos-ai](https://pypi.org/project/bos-ai/).

## Why does this exist?

Two reasons, one of which became the main one in 2.0.0.

**The command name has to match the PyPI name.** Tool runners like `uvx` and `pipx` assume the command you want matches the package name (running `uvx command` expects a package named `command` on PyPI). The library is published as `bos-ai`, so `uvx boscli` needed a package actually called `boscli`.

**As of 2.0.0, `bos-ai` ships no console script at all.** It is a library install — about 14 MB, no CLI dependencies, no terminal UI — so that it can be embedded in another application without dragging in `click`, `rich` and `textual`. This package is now the only packaged `boscli` command. (A `pip install 'bos-ai[cli]'` gets the CLI's dependencies without this shim, and runs it as `python -m bos.cli`.)

## Usage

You can run the CLI immediately without manual installation using `uvx` or `pipx`:

```bash
# Run one-off commands dynamically
uvx boscli ask "how does this work?"

# Alternatively using pipx
pipx run boscli ask "how does this work?"
```

To install the CLI globally on your system:

```bash
# Using uv
uv tool install boscli

# Using pipx
pipx install boscli
```

## How It Works

This project contains no functional python code of its own. Its `pyproject.toml` simply:
1. Declares a dependency on `bos-ai[cli,litellm,search]` — `cli` for `click`/`rich`/`textual` (and, recursively, the gateway's `aiohttp`), `litellm` for the built-in LLM provider, `search` for the built-in web-search tools that the default configuration enables. `lark` is left out: a 98 MB SDK for one channel, opt-in via `pip install 'bos-ai[lark]'`.
2. Maps the `boscli` console script directly to the entrypoint defined inside `bos-ai`:
   ```toml
   [project.scripts]
   boscli = "bos.cli.entry:main"
   ```

### Automated Updates
A GitHub Actions workflow checks PyPI for new releases of `bos-ai` daily. When a new version is detected, the workflow automatically updates this package's version and dependency pin, commits and pushes to the main branch, tags the commit, and publishes the new matching version of `boscli` to PyPI. 

This ensures `uvx boscli` always runs the latest version of `bos-ai` automatically.
