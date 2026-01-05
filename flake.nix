{
  description = "Dev flake for lazyclone";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-25.11";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs;
        builtins.concatLists [
          [
            python313
            uv
          ]
        ];

      shellHook = ''
        uv sync
      '';
    };
  };
}
