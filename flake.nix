{
  description = "Yet another pretty printer for tables and trees";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nix-utils.url = "github:padhia/nix-utils";

  outputs = { nixpkgs, flake-utils, nix-utils, ... }:
  let
    inherit (nix-utils.outputs.lib) pyDevShell extendPyPkgsWith;

    overlays.default = final: prev:
      extendPyPkgsWith prev {
        yappt = ./yappt.nix;
      };

    eachSystem = system:
    let
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.default = pyDevShell {
        inherit pkgs;
        name = "yappt";
      };
    };

  in {
    inherit overlays;
    inherit (flake-utils.lib.eachDefaultSystem eachSystem) devShells;
  };
}
