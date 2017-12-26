export GITAWAREPROMPT=~/dotfiles/git-aware-prompt
. "$GITAWAREPROMPT/main.sh"

_host=""
if [ -n "$SSH_CONNECTION" ]; then
    _host="\h:"
fi
export PS1="[\t] $_host\W\${git_branch:+ \[$txtgrn\]\$git_branch\[$txtred\]\$git_dirty\[$txtrst\]}\$ "
unset _host

export EDITOR="subl --wait --new-window"
export OPENPY_EDITOR="subl"

export LSCOLORS=ExGxBxDxCxEgEdxbxgxcxd
export CLICOLOR=1
export GREP_OPTIONS='--color=auto'
export GREP_COLOR='1;31'
