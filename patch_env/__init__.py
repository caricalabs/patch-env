"""
Imported by patch_env.pth to patch the environment when PATCH_ENV_COMMAND is set.
"""
import os

var = 'PATCH_ENV_COMMAND'
cmd = os.environ.get(var)
if cmd:
    import subprocess
    import logging

    proc = subprocess.run(cmd, shell=True, capture_output=True)
    if proc.returncode != 0:
        logging.warning(f'{var} failed with status {proc.returncode}')
        if proc.stderr:
            logging.warning(proc.stderr)
        if proc.stdout:
            logging.warning(proc.stdout)
    else:
        for line in str(proc.stdout, 'utf-8').splitlines():
            parts = line.split('=', 1)
            if len(parts) != 2:
                logging.error(f'Ignoring invalid output from {var}: {line}')
            else:
                logging.debug(line)
                os.environ[parts[0]] = parts[1]
