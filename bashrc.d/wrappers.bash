# Wrappers around built-in commands

alias mv='mv -i'
alias cp='cp -i'
alias cd='pushd >/dev/null'
alias fail='tail -f'

alias ssh="~/dotfiles/color-ssh/color-ssh.py"

function mcd {
    mkdir -p "$1"
    cd "$1"
}

alias reload='exec bash'
