# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2026-01-10

### Added

- Links to commit history from changelog.
- README badges.

### Changed

- CI will no longer publish on every push to the main branch.

### Fixed

- Error caused by incorrectly passing SSH argument.
- Broken SSH repository resolution.

## [0.2.0] - 2026-01-10

### Added

- Support for other default hosts with `--host` argument.
- Support for defaulting to clone with SSH with `--ssh` flag.
- SSH shorthand starting with `@` (e.g., `@owner/repo`).
- Support for flake-like repository references (e.g., `github:owner/repo`).
- Documentation of development workflow in `CONTRIBUTING.md`.
- Nix-based build job in CI.
- Support for `taplo` (TOML), `alejandra` (Nix), `yamlfmt` (YAML), and `mdformat` (Markdown) formatters.
- Unified `fmt` command in Nix development shell for project-wide formatting.
- Dedicated GitHub Actions workflow for linting TOML, Nix, YAML, and Markdown.

### Changed

- Run checks on pushes and PRs to all branches.
- Migrated Python linting and formatting from `flake8` to `ruff`.

## [0.1.0] - 2026-01-08

### Added

- Initial release.
- Support for lazy cloning from GitHub with search.
- Support for opening cloned repository with program.
- Nix flake installation.
- Nix flake development environment.

[0.1.0]: https://github.com/olillin/lazyclone/commits/0.1.0
[0.2.0]: https://github.com/olillin/lazyclone/compare/0.1.0...0.2.0
[0.2.1]: https://github.com/olillin/lazyclone/compare/0.2.0...0.2.1
[unreleased]: https://github.com/olillin/lazyclone/compare/0.2.1...dev
