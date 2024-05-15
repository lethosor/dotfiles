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
GIT_PS1_STATESEPARATOR=" "
GIT_PS1_SHOWUNTRACKEDFILES=1

HISTSIZE=10000
HISTFILESIZE=10000
PROMPT_COMMAND="history -a; $PROMPT_COMMAND"

export EDITOR="subl --wait --new-window"
export OPENPY_EDITOR="subl"

export LSCOLORS=ExGxBxDxCxEgEdxbxgxcxd
export CLICOLOR=1
export GREP_COLOR='1;31'
export GREP_COLORS='mt=1;31' # GNU grep 3.8+

export CDPATH=

if ps -p $(ps -p $$ -o ppid=) -o cmd 2>/dev/null | grep gnome-terminal >/dev/null; then
    PROMPT_COMMAND="reset-title \"\$(basename \"\$(pwd)\")\"; $PROMPT_COMMAND"
fi

function reload {
    if [ -n "$bash_profile_loaded" ]; then
        . ~/.bash_profile
    else
        . ~/.bashrc
    fi
}

function reload_all {
    date > ~/bashrc.d/.reload-all.date
    _reload_all_check
}
alias reload-all=reload_all

function _reload_all_check {
    local _reload_all_cur="$(cat ~/bashrc.d/.reload-all.date 2>/dev/null)"
    if [[ "$_reload_all_cur" != "$_reload_all_last" ]]; then
        if [[ -n "$_reload_all_last" ]]; then
            echo "reload-all: updating $_reload_all_last -> $_reload_all_cur"
            export _reload_all_last="$_reload_all_cur"
            reload
        fi
        export _reload_all_last="$_reload_all_cur"
    fi
}
_reload_all_check
PROMPT_COMMAND="_reload_all_check; $PROMPT_COMMAND"

if [[ -t 0 ]]; then
    PROMPT_COMMAND="stty $(stty -g); $PROMPT_COMMAND"
fi
