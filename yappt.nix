{
  lib,
  buildPythonPackage,
  setuptools,
  pytest,
}:
buildPythonPackage {
  pname = "yappt";
  version = "0.3.2";
  pyproject = true;
  src = ./.;

  build-system = [ setuptools ];
  nativeCheckInputs = [ pytest ];

  meta = with lib; {
    homepage    = "https://github.com/padhia/yappt";
    description = "Yet another pretty printer for tables and trees";
    maintainers = with maintainers; [ padhia ];
  };
}
