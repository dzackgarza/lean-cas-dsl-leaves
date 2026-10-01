# The leaves are a manifest (`leaves.json`) and Python backend programs; they ship no Lean.
# These tiers check only that the manifest is JSON and the programs compile.

# List available recipes.
default:
    @just --list

# Check the manifest and the backend programs.
test-commit:
    python3 -m json.tool leaves.json > /dev/null
    python3 -m py_compile backends/*.py

# Same as the commit tier.
test-push: test-commit

# Same as the commit tier.
test-ci: test-commit
