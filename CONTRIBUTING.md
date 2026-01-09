# Contributing

Thank you for your interest in contributing to lazyclone!

All contributions are welcome, whether it be bug reports, feature requests, or pull requests.

## How to Develop

### Nix Flakes

The recommended workflow is to use Nix Flakes to build the project and manage the environment.

If you don't already have nix installed, you can install it from the [official downloads page](https://nixos.org/download.html).

If you wish to build without nix, you can also use the `uv` commands described below.

### Installing dependencies

To enter a [Nix shell](https://nix.dev/manual/nix/stable/command-ref/nix-shell.html) with all dependencies installed, run:

```bash
nix develop
```

Without Nix flakes, create a virtual environment:

```bash
uv venv
```

Then activate it with the command in the output.

To install the dependencies globally, run:

```bash
uv pip install --system .
```

### Building

With Nix flakes:

```bash
nix build
```

Without Nix flakes:

```bash
uv build
```

The resulting binary will be `./result/bin/lazyclone`.

### Running tests

```bash
python -m unittest discover tests
```
