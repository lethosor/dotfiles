# Wrappers around built-in commands

alias fail='tail -f'
alias la='ls -A'
alias ll='ls -alF'
alias node="node --experimental-repl-await"
alias ping='ping -c 1000'

alias ssh="~/dotfiles/color-ssh/color-ssh.py"

function _default_confirm_arg {
    local cmd="$1"
    local args='-i'
    shift
    local opt OPTIND
    while getopts ":ifn" opt; do
        case "$opt" in
            '?') ;;
            *) args= ;;
        esac
    done
    command "$cmd" $args "$@"
}
alias cp='_default_confirm_arg cp'
alias mv='_default_confirm_arg mv'

function cd {
    pushd -n "$(pwd)" >/dev/null
    command cd "$@"
}

function reload {
    if [ -n "$bash_profile_loaded" ]; then
        . ~/.bash_profile
    else
        . ~/.bashrc
    fi
}

function mcd {
    mkdir -p "$1"
    cd "$1"
}

function unsafe-ssh {
    ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$@"
}

function txa {
    tmux attach -t "$1" 2>/dev/null || tmux new -s "$1"
}
alias txs=tmux-shell
