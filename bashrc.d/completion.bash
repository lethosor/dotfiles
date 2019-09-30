[ -n "$HOMEBREW_PREFIX" ] && src_if_exists "$HOMEBREW_PREFIX/etc/bash_completion"

if PATH="$HOME/bin" cmd_exists git; then
    # local git install, use local git completion too
    . "$HOME/dotfiles/deps/git-completion.bash"
fi

_git_ancestor() {
    __git_complete_refs $track_opt
}

_git_count_commits() {
    test $cword = 2 && __gitcomp_nl "$(__git_remotes)"
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

# disable unzip/tar completion to allow files with unconventional extensions
complete -r tar unzip 2>/dev/null
if [[ "$(type -t _minimal)" = "function" ]]; then
    # on linux, completions will be redefined automatically if undefined
    complete -F _minimal tar unzip
fi

_pyshell() {
    local word="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=($(compgen -W "$(ls ~/.config/pyshell/*.py 2>/dev/null | while read line; do basename "$line"; done | cut -d. -f1)" -- "$word"))
} && complete -F _pyshell pyshell

_tmux_list_sessions() {
    local word="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=($(compgen -W "$(tmux ls 2>/dev/null | cut -d: -f1)" -- "$word"))
} && complete -F _tmux_list_sessions txa

_tmux_shell() {
    local word="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=($(compgen -W "$(ls ~/.config/tmux-shell/ 2>/dev/null)" -- "$word"))
} && complete -F _tmux_shell tmux-shell txs

_workon_fallback() {
    local word="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=($(compgen -W "$(find ~/.virtualenvs/ -mindepth 1 -maxdepth 1 -type d 2>/dev/null | while read line; do basename "$line"; done)" -- "$word"))
}
if ! complete -p workon >/dev/null 2>&1; then
    complete -F _workon_fallback workon
fi

for cmd in kubectl minikube; do
    if cmd_exists "$cmd"; then
        . <("$cmd" completion bash 2>/dev/null)
    fi
done
