{ lib, buildPythonPackage, setuptools, pytest }:

buildPythonPackage rec {
  pname = "yappt";
  version = "0.3.0";
  pyproject = true;
  src = ./.;

  nativeBuildInputs = [
    setuptools
  ];

  nativeCheckInputs = [
    pytest
  ];

  meta = with lib; {
    homepage = "https://github.com/padhia/yappt";
    description = "Yet another pretty print for tables and trees";
    maintainers = with maintainers; [ padhia ];
  };
}
