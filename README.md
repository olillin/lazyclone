# lazyclone

[![GitHub branch check runs](https://img.shields.io/github/check-runs/olillin/lazyclone/main?style=flat-square)](https://github.com/olillin/lazyclone/actions)
[![PyPI - Version](https://img.shields.io/pypi/v/lazyclone?style=flat-square&logo=Python&logoColor=white)](https://pypi.org/project/lazyclone)

Git clone but easier. Built as a replacement/improvement of my project, [clode](https://github.com/olillin/clode).

Clone a repository without the full URL:

```console
$ lazyclone olillin/lazyclone
Cloning https://github.com/olillin/lazyclone
```

If [GitHub CLI](https://cli.github.com) is installed lazyclone will detect your
GitHub username:

```console
$ lazyclone bonk
Cloning https://github.com/olillin/bonk
```

If there are multiple options you will be able to choose which repository to clone:

```console
$ lazyclone lazy
[?] Select repository to clone: 
 > olillin/lazyclone
   LazyVim/LazyVim
   l123456789jy/Lazy
   jesseduffield/lazygit
   jesseduffield/lazydocker
   aFarkas/lazysizes
```

You can even tell lazyvim to immediately open your favorite editor after cloning:

```console
$ lazyclone bonk --program nvim
Cloning https://github.com/olillin/bonk
Successfully cloned into 'bonk'
Launching nvim...
```

See [Usage](#usage) for more details.

## Installation

### Pip

To install using **pip** simply run the command below:

```console
pip install lazyclone
```

### Nix/NixOS

**lazyclone** can be installed using [Nix Flakes](#nix-flakes), see the section below.

#### Nix Flakes

Add the required inputs to your flake configuration:

`flake.nix`

```nix
{
  description = "NixOS configuration with lazyclone";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-25.11";

    lazyclone = {
      url = "github:olillin/lazyclone";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    ...
  } @ inputs: {
    nixosConfigurations.yourconfiguration = nixpkgs.lib.nixosSystem {
      specialArgs = {inherit inputs;};
      modules = [
        ./configuration.nix
      ];
    };
  };
}
```

Install the package in your `configuration.nix` or an imported module:

`configuration.nix`

```nix
{
  pkgs,
  inputs,
  ...
}: {
  environment.systemPackages = with pkgs; [
    inputs.lazyclone.packages.${pkgs.stdenv.hostPlatform.system}.default
  ];
}
```

## Usage

### Arguments

| Argument | Type | Description | Example value |
|------------------|--------|----------------------------------------------|---------------------|
| `repo` | string | Name or query of the repository to clone | `olillin/lazyclone` |
| `directory` | string | Directory the repository should be cloned to | `lazyclone-2` |
| `-h`/`--help` | flag | Show the help menu | |
| `-p`/`--program` | string | Program to open the cloned repository with | `code` |
| `--host` | string | URL for default git provider | `https://github.com`|
| `--ssh` | flag | Prefer SSH over HTTPS | |
| `--debug` | flag | Enable debug logs | |

### Help message

```console
usage: lazyclone [-h] [-p PROGRAM] [--host HOST] [--ssh] [--debug]
                 repo [directory]

Clone Git repositories easier

positional arguments:
  repo                  url or name of repository to clone
  directory             the name of a new directory to clone into

options:
  -h, --help            show this help message and exit
  -p, --program PROGRAM
                        open with this program after cloning
  --host HOST           URL for default git host (default: https://github.com)
  --ssh                 prefer ssh over https
  --debug               enable debugging output
```
