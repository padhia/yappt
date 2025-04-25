{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.pyproject-nix.url = "github:pyproject-nix/pyproject.nix";

  inputs.pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";

  outputs = { self, nixpkgs, flake-utils, pyproject-nix, ... }:
  let
    inherit (nixpkgs.lib) composeManyExtensions;

    project = pyproject-nix.lib.project.loadPyproject {
      projectRoot = ./.;
    };

    pkgOverlay = final: prev: {
      pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
        (py-final: py-prev: {
          yappt = project.renderers.buildPythonPackage { inherit py-final; };
        })
      ];
    };

    overlays.default = composeManyExtensions [
      pkgOverlay
    ];

    buildSystem = system:
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
    inherit (flake-utils.lib.eachDefaultSystem buildSystem) devShells;
  };
}
