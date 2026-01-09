# Contributing

Thank you for your interest in contributing to lazyclone!

All contributions are welcome, whether it be bug reports, feature requests, or pull requests.

## How to Develop

### Nix Flakes

The recommended workflow is to use Nix Flakes to build the project and manage the environment.

To enter a shell with all dependencies installed, run:

```bash
nix develop
```

> Note: If you don't have nix installed, you can install it from [here](https://nixos.org/download.html).

If you wish to build without nix, you can use the `uv` commands described below.

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
