{
  description = "Build Python package yappt";

  inputs.nixpkgs.url     = "github:nixos/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
  flake-utils.lib.eachDefaultSystem (system:
  let
    pkgs    = nixpkgs.legacyPackages.${system};
    pythons = ["python311" "python312"];
    python3 = pkgs.lib.replaceStrings ["."] [""] pkgs.python3.libPrefix;

    pyModules = py:
      let
        callPackage = pkgs.lib.callPackageWith pkgs.${py}.pkgs;
      in {
        yappt = callPackage ./yappt.nix {};
      };

    devShells =
      let
        mkDevShell = py:
          pkgs.mkShell {
            name = "yappt";
            venvDir = "./.venv";
            buildInputs = with pkgs.${py}.pkgs; [
              pkgs.${py}
              pkgs.ruff
              venvShellHook
              build
              pytest
            ];
          };
        allPyDevs = pkgs.lib.genAttrs pythons mkDevShell;
      in allPyDevs // {
        default = allPyDevs.${python3};
      };

    packages =
      let
        mkPackage = py: {
          name  = "${py}Packages";
          value = pyModules py;
        };
      in
        builtins.listToAttrs (builtins.map mkPackage pythons);

  in {
    inherit devShells packages;
  });
}
