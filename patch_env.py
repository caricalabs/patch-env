"""
Intercept the loading of a module, patch `os.environ` using the output
of a specified program, then resume loading the specified module.
"""

import os
import subprocess
import sys

cmd = os.environ.get('PATCH_ENV_COMMAND')
if not cmd:
    print(
        'PATCH_ENV_COMMAND must be set to a shell command that prints lines like VAR=value',
        file=sys.stderr,
    )
    sys.exit(2)

proc = subprocess.run(cmd, shell=True, capture_output=True)
if proc.returncode != 0:
    print(f'PATCH_ENV_COMMAND failed with code {proc.returncode}', file=sys.stderr)
    sys.stdout.write(str(proc.stdout, 'utf-8'))
    sys.stderr.write(str(proc.stderr, 'utf-8'))
    sys.exit(3)

for line in str(proc.stdout, 'utf-8').splitlines():
    print(line)
    name, value = line.split('=', 1)
    os.environ[name] = value

# Remove this module's directory from the interpreter's search path.

this_module = sys.modules[__name__]
this_module_dir = os.path.dirname(this_module.__file__)

sys.path.remove(this_module_dir)

# Import the aliased module's implementation.

import importlib

importlib.reload(this_module)
