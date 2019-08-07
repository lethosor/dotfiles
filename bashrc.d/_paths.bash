add_path PATH begin /usr/local/sbin /usr/local/bin
add_path PATH begin ~/bin ~/dotfiles/bin

add_path PYTHONPATH begin ~/bin/python

export GOPATH=~/go
add_path PATH end "$GOPATH/bin"

add_path PATH end ~/dotfiles/bin/shims
