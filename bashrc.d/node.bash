nvm_sh="$HOME/.nvm/nvm.sh"
if [[ -f "$nvm_sh" ]]; then
    if cmd_exists realpath; then
        nvm_sh="$(realpath "$nvm_sh")"
    fi
    . "$nvm_sh"
fi

if cmd_exists npm && ! complete -p npm >/dev/null 2>&1; then
    . <(npm completion)
fi
