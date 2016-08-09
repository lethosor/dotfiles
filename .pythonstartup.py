import sys
try:
    import readline
    import rlcompleter
except ImportError:
    pass
else:
    is_libedit = False
    if sys.platform.startswith('darwin'):
        if sys.executable.startswith('/System') or sys.executable.startswith('/usr/bin'):
            is_libedit = True
    if not is_libedit:
        readline.parse_and_bind("tab: complete")
    else:
        readline.parse_and_bind("bind ^I rl_complete")
