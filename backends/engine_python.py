"""Load the research container's SageMath engine (`/sage/.venv/bin/python3`)."""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from types import ModuleType

_CONTAINER_PYTHON = Path("/sage/.venv/bin/python3")
_REEXEC = "CAS_LEAVES_ENGINE_REEXEC"


def require_engine(_env_var: str = "", modules: tuple[str, ...] = ("sage.all",)) -> ModuleType:
    for module in modules:
        try:
            return importlib.import_module(module)
        except ModuleNotFoundError as exc:
            if exc.name not in {module, module.split(".")[0]}:
                raise
    if not os.environ.get(_REEXEC) and _CONTAINER_PYTHON.is_file() and os.access(_CONTAINER_PYTHON, os.X_OK):
        script = os.path.abspath(sys.argv[0])
        env = dict(os.environ, **{_REEXEC: "1"})
        os.execve(str(_CONTAINER_PYTHON), [str(_CONTAINER_PYTHON), script, *sys.argv[1:]], env)
    joined = " or ".join(modules)
    sys.stderr.write(f"{sys.argv[0]}: {joined} is not importable under {sys.executable}\n")
    sys.exit(1)
