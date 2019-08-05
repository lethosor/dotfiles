export PYTHONSTARTUP=~/.pythonstartup.py

# do this before setting up pyenv
if [ -z "$VIRTUALENVWRAPPER_PYTHON" ]; then
    export VIRTUALENVWRAPPER_PYTHON="$(which python)"
fi

export PYENV_ROOT="$HOME/.pyenv"
add_path PATH begin "$PYENV_ROOT/bin" "$PYENV_ROOT/shims"
if cmd_exists pyenv; then
    old_path="$PATH"
    eval "$(pyenv init -)"
    export PATH="$old_path"
    unset old_path
fi

if cmd_exists virtualenvwrapper_lazy.sh; then
    . "$(which virtualenvwrapper_lazy.sh)"
fi
