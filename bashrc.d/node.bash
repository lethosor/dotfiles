nvm_sh="$HOME/.nvm/nvm.sh"
if [[ -f "$nvm_sh" ]]; then
    if cmd_exists realpath; then
        nvm_sh="$(realpath "$nvm_sh")"
    fi
    . "$nvm_sh"
fi

cmd_exists npm && . <(npm completion)
