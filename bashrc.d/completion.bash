[ -n "$HOMEBREW_PREFIX" ] && src_if_exists "$HOMEBREW_PREFIX/etc/bash_completion"

_git_ancestor() {
    __git_complete_refs $track_opt
}

_git_vpush() {
    words[1]=push
    _git_push "$@"
}
