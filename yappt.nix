{ lib, buildPythonPackage, setuptools, pytest }:
buildPythonPackage rec {
  pname     = "yappt";
  version   = "0.3.2";
  pyproject = true;
  src       = ./.;

  nativeBuildInputs = [ setuptools pytest ];
  doCheck           = false;

  meta = with lib; {
    homepage    = "https://github.com/padhia/yappt";
    description = "Yet another pretty printer for tables and trees";
    maintainers = with maintainers; [ padhia ];
  };
}
