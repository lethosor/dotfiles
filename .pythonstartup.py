import sys
py3 = sys.version.startswith('3')
try:
    import readline
    import rlcompleter
except ImportError:
    pass
else:
    if py3:
        readline.parse_and_bind("tab: complete")
    else:
        readline.parse_and_bind("bind ^I rl_complete")
