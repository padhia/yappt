{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
  let
    overlays.default = final: prev: {
      pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
        (py-final: py-prev: {
          yappt = py-final.callPackage ./yappt.nix {};
        })
      ];
    };

    eachSystem = system:
    let
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
        overlays = [ self.overlays.default ];
      };

      pyPkgs = pkgs.python312Packages;

    in {
      devShells.default = pkgs.mkShell {
        name = "yappt";
        venvDir = "./.venv";
        buildInputs = with pyPkgs; [
          pkgs.ruff
          pkgs.uv
          python
          venvShellHook
          pytest
        ];
      };
    };

  in {
    inherit overlays;
    inherit (flake-utils.lib.eachDefaultSystem eachSystem) devShells;
  };
}
