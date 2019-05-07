. "$HOME/dotfiles/deps/git-prompt.sh"

_host=""
if [ -n "$SSH_CONNECTION" ]; then
    _host="\h:"
fi
export PS1="[\t] $_host\W\$ "
PROMPT_COMMAND="__git_ps1 '\${VIRTUAL_ENV:+(\$(basename \$VIRTUAL_ENV)) }[\t] $_host\W' '\\\$ '; $PROMPT_COMMAND"
unset _host

GIT_PS1_SHOWCOLORHINTS=1
GIT_PS1_SHOWDIRTYSTATE=1
GIT_PS1_STATESEPARATOR=
GIT_PS1_SHOWUNTRACKEDFILES=1

export EDITOR="subl --wait --new-window"
export OPENPY_EDITOR="subl"

export LSCOLORS=ExGxBxDxCxEgEdxbxgxcxd
export CLICOLOR=1
export GREP_COLOR='1;31'

export CDPATH=
