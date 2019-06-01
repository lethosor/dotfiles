export PYTHONSTARTUP=~/.pythonstartup.py

# do this before setting up pyenv
if [ -z "$VIRTUALENVWRAPPER_PYTHON" ]; then
    export VIRTUALENVWRAPPER_PYTHON="$(which python)"
fi

export PYENV_ROOT="$HOME/.pyenv"
add_path PATH begin "$PYENV_ROOT/bin"
if cmd_exists pyenv; then
    eval "$(pyenv init -)"
fi
