{
  description = "Build Python package yappt";
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, flake-utils }:
  let
    forAllSystems = fn:
      let
        systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      in
        nixpkgs.lib.genAttrs systems (system: fn (import nixpkgs { inherit system; }));

    pyPkgs = { pkgs, python3 }:
      let
        callPackage = pkgs.lib.callPackageWith (pkgs // python3.pkgs);
      in {
        yappt = callPackage ./yappt.nix {};
      };

    devShells = forAllSystems (pkgs: with pkgs;
      { default = pkgs.mkShell {
          name = "yappt";
          venvDir = "./.venv";
          buildInputs = with pkgs.python311Packages; [
            python
            venvShellHook
            build
            pytest
            pkgs.ruff
          ];
        };
      }
    );

    packages = forAllSystems (pkgs: with pkgs; { default = (pyPkgs { inherit pkgs; python3 = python311; }).yappt; });

  in {
    inherit devShells packages pyPkgs;
  };
}
