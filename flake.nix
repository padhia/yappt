{
  description = "Yet another pretty printer for tables and trees";

  inputs = {
    nixpkgs.url   = "github:nixos/nixpkgs/nixos-unstable";
    nix-utils.url = "github:padhia/nix-utils";

    nix-utils.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, nix-utils }:
    nix-utils.lib.mkPyFlake {
      pkgs = { yappt = import ./yappt.nix; };
      deps = [ "pytest" ];
    };
}
