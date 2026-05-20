# boscli

[![Release to PyPI](https://github.com/bos-agent/boscli/actions/workflows/release.yml/badge.svg)](https://github.com/bos-agent/boscli/actions/workflows/release.yml)
[![Sync with bos-ai](https://github.com/bos-agent/boscli/actions/workflows/sync.yml/badge.svg)](https://github.com/bos-agent/boscli/actions/workflows/sync.yml)

A thin CLI shim package for [bos-ai](https://pypi.org/project/bos-ai/).

## Why does this exist?

The primary PyPI package is published as `bos-ai`, but it exposes the console script executable named `boscli`. 

Tool runners like `uvx` and `pipx` assume by default that the command you want to run matches the PyPI package name (e.g., running `uvx command` expects a package named `command` on PyPI). 

Because the package (`bos-ai`) and the script (`boscli`) names differed, running `uvx boscli` did not work out of the box. This `boscli` package solves this by serving as a lightweight redirect/wrapper that depends directly on `bos-ai` and exposes the `boscli` console entrypoint.

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
1. Declares a dependency on `bos-ai`.
2. Maps the `boscli` console script directly to the entrypoint defined inside `bos-ai`:
   ```toml
   [project.scripts]
   boscli = "bos.cli.entry:main"
   ```

### Automated Updates
A GitHub Actions workflow checks PyPI for new releases of `bos-ai` every 6 hours. When a new version is detected, the workflow automatically updates this package's version and dependency pin, commits and pushes to the main branch, tags the commit, and publishes the new matching version of `boscli` to PyPI. 

This ensures `uvx boscli` always runs the latest version of `bos-ai` automatically.
