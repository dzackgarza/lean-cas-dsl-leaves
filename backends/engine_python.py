"""Start a backend program under the Python interpreter that has its engine.

The kernel starts a backend with the fixed command of its manifest entry (`python3`), which cannot
name an interpreter by environment. When the engine is not importable there, the program re-runs
itself under `$<env_var>`, or else the first `.venv/bin/python` found in the working directory or
one of its parents (the running workspace: the kernel runs a backend in the manifest's directory,
`<workspace>/.lake/packages/cas_leaves`). If no interpreter has the engine, the program exits
before announcing itself, and the kernel reports the backend unavailable.
"""

import importlib
import os
import sys
from pathlib import Path

_REEXEC = "CAS_LEAVES_ENGINE_REEXEC"


def _candidates(env_var):
    configured = os.environ.get(env_var)
    if configured:
        yield Path(configured)
    cwd = Path.cwd()
    for directory in (cwd, *cwd.parents):
        yield directory / ".venv" / "bin" / "python"


def require_engine(env_var, module):
    """Import `module`, or re-run this program under an interpreter that can."""
    try:
        importlib.import_module(module)
        return
    except ImportError as exc:
        missing = exc
    if os.environ.get(_REEXEC):
        sys.stderr.write("%s: %s is not importable under %s: %s\n"
                         % (sys.argv[0], module, sys.executable, missing))
        sys.exit(1)
    for python in _candidates(env_var):
        if python.is_file() and os.access(python, os.X_OK):
            script = os.path.abspath(sys.argv[0])
            env = dict(os.environ, **{_REEXEC: "1"})
            os.execve(str(python), [str(python), script, *sys.argv[1:]], env)
    sys.stderr.write("%s: %s is not importable, and no interpreter was found ($%s, or "
                     ".venv/bin/python of the workspace): %s\n"
                     % (sys.argv[0], module, env_var, missing))
    sys.exit(1)
