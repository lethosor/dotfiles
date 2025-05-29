# adapted from https://github.com/int3h/SublimeFixMacPath/blob/master/FixPath.py

import os
import subprocess

old_env = {}

def plugin_loaded():
    for key in {'PATH'}:
        old_env[key] = os.environ[key]

    os.environ['PATH'] = subprocess.check_output(['bash', '-l', '-c', 'source ~/dotfiles/.bashrc; printf "%s" "$PATH"']).decode()

def plugin_unloaded():
    for key in old_env:
        os.environ[key] = old_env[key]
