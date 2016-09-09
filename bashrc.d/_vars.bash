# Local vars
if cmd_exists brew; then
    HOMEBREW_PREFIX="$(brew --prefix)"
fi

# Exported vars
export PROMPT_COMMAND=""
