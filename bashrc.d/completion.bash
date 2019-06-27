[ -n "$HOMEBREW_PREFIX" ] && src_if_exists "$HOMEBREW_PREFIX/etc/bash_completion"

if PATH="$HOME/bin" cmd_exists git; then
    # local git install, use local git completion too
    . "$HOME/dotfiles/deps/git-completion.bash"
fi

_git_ancestor() {
    __git_complete_refs $track_opt
}

_git_fetch_pr() {
    test $cword = 2 && __gitcomp_nl "$(__git_remotes)"
}

_git_prune_branches() {
    case "$cur" in
        --*) __gitcomp "--force --dry-run" ;;
    esac
}

_git_rprune() {
    test $cword = 2 && __gitcomp_nl "$(__git_remotes)"
}

_git_vpush() {
    words[1]=push
    _git_push "$@"
}

cmd_exists npm && . <(npm completion)
