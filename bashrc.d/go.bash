if [ -n "$HOMEBREW_PREFIX" ]; then
    export GOROOT="$HOMEBREW_PREFIX/opt/go/libexec"
elif [ -d "$HOME/.local/go" ]; then
    export GOROOT="$HOME/.local/go"
fi

export GOPATH=~/go
export GOBIN="$GOPATH/bin"

add_path PATH end "$GOROOT/bin" "$GOPATH/bin"
