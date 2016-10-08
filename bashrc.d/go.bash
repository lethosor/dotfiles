if [ -n "$HOMEBREW_PREFIX" ]; then
    export GOROOT="$HOMEBREW_PREFIX/opt/go/libexec"
fi

if [ -n "$GOPATH" ]; then
    export GOBIN="$GOPATH/bin"
fi
