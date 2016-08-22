export GITAWAREPROMPT=~/dotfiles/git-aware-prompt
. "$GITAWAREPROMPT/main.sh"

export PS1="[\t] \W\${git_branch:+ \[$txtgrn\]\$git_branch\[$txtred\]\$git_dirty\[$txtrst\]}\$ "

export EDITOR="subl --wait --new-window"

export LSCOLORS=ExGxBxDxCxEgEdxbxgxcxd
export CLICOLOR=1
export GREP_OPTIONS='--color=auto'
export GREP_COLOR='1;31'
