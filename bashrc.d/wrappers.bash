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

# maintain "-bash" vs "bash"
if [[ "$(ps -p $$ -o command | tail -n1)" =~ ^- ]]; then
    alias reload='test -n "$VIRTUAL_ENV" && deactivate; exec -l bash'
else
    alias reload='test -n "$VIRTUAL_ENV" && deactivate; exec bash'
fi

function txa {
    tmux attach -t "$1" 2>/dev/null || tmux new -s "$1"
}
alias txs=tmux-shell
