[doc("List available recipes.")]
default:
    @just --list

[doc("Check manifest JSON, backend compilation, and leaf-boundary hygiene.")]
test:
    python3 -m json.tool leaves.json > /dev/null
    python3 -m py_compile backends/*.py
    ! grep -rn 'CasElaborator\|tests/acceptance' backends/ --include='*.py'

[private]
test-commit: test

[private]
test-push: test

[doc("Run CI quality gate.")]
test-ci: test
