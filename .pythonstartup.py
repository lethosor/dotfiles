import sys
try:
    import readline
    import rlcompleter
except ImportError:
    pass
else:
    is_libedit = ('libedit' in readline.__doc__.lower())
    if not is_libedit:
        readline.parse_and_bind("tab: complete")
    else:
        readline.parse_and_bind("bind ^I rl_complete")
