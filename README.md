# Oberon0 Runtime for WebAssembly

![Made at HEIA-FR](https://img.shields.io/badge/Made%20at-HEIA--FR-blue)
![Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fheiafr-isc%2Foberon0-runtime-py%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)
![CI](https://img.shields.io/github/actions/workflow/status/heiafr-isc/oberon0-runtime-py/ci.yml?label=CI)
![Docs](https://img.shields.io/github/actions/workflow/status/heiafr-isc/oberon0-runtime-py/docs.yml?label=Docs)
[![REUSE status](https://api.reuse.software/badge/github.com/heiafr-isc/oberon0-runtime-py)](https://api.reuse.software/info/github.com/heiafr-isc/oberon0-runtime-py)

Oberon0 Runtime is a Python CLI runtime for executing WebAssembly modules generated from Oberon0 programs.

It provides:

- a command to list exported functions from a WASM module,
- a command to execute a selected function,
- runtime host functions compatible with the Oberon0 runtime model (input/output and memory support).

Project documentation: https://heiafr-isc.github.io/oberon0-runtime-py/

## Features

- CLI built with `typer`
- Runtime execution powered by `wasmtime`
- Rich terminal output for command discovery (`info` command)
- Input buffering for integer-based program input
- Type/lint/test tooling (`ruff`, `black`, `pyright`, `mypy`, `pytest`)

## Requirements

- Python `>= 3.12`
- `uv` for dependency and task management

Optional (for examples/tests using `.wat` sources):

- `wabt` (`wat2wasm`)

## Installation

### From source

```bash
git clone https://github.com/heiafr-isc/oberon0-runtime-py.git
cd oberon0-runtime-py
uv sync
```

### Install CLI tool in your environment

```bash
uv tool install .
```

After that, the CLI is available as:

```bash
oberon0-rt --help
```

## Command-Line Usage

### Show available commands in a WASM module

```bash
oberon0-rt info <module.wasm>
```

### Run a command exported by a WASM module

```bash
oberon0-rt run <module.wasm> <command> [numbers...]
```

### Enable debug logs

```bash
oberon0-rt run <module.wasm> <command> [numbers...] --debug
```

## Quick Example

Compile an example `.wat` file and run it:

```bash
wat2wasm -o tests/add.wasm examples/add.wat
oberon0-rt info tests/add.wasm
oberon0-rt run tests/add.wasm add 29 13
```

Expected result for the last command: `42`

## Development

Install development dependencies:

```bash
uv sync --group dev
```

Run checks:

```bash
uv run ruff check .
uv run black --check .
uv run pyright
uv run mypy src tests
```

Run tests:

```bash
uv run pytest
```

Build package:

```bash
uv build
```

## Documentation

Build docs locally:

```bash
uv run sphinx-build -M html docs public
```

or via `just`:

```bash
just make-doc
```

Generated HTML will be available in `public/html`.

## CI/CD

The repository uses GitHub Actions workflows split by concern:

- `ci.yml`: static analysis, build, and tests
- `docs.yml`: documentation build and GitHub Pages deployment
- `docker.yml`: Docker image build and push to GHCR

`docs.yml` and `docker.yml` are triggered by `workflow_run` after successful CI.

## Repository Layout

```text
src/oberon0_runtime/   Python package
tests/                 Test suite
examples/              Sample WAT input files
docs/                  Sphinx documentation
.github/workflows/     CI/CD pipelines
```

## License

This project is licensed under the MIT license.

See:

- `LICENSES/MIT.txt`
- `REUSE.toml`
