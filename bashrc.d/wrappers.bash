# Wrappers around built-in commands

alias mv='mv -i'
alias cp='cp -i'
alias fail='tail -f'

alias ssh="~/dotfiles/color-ssh/color-ssh.py"

function cd {
    pushd -n "$(pwd)" >/dev/null
    command cd "$@"
}

function mcd {
    mkdir -p "$1"
    cd "$1"
}

function unsafe-ssh {
    ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$@"
}

alias reload='exec bash'
