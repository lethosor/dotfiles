if [ -n "$HOMEBREW_PREFIX" ]; then
    add_path PATH begin "$HOMEBREW_PREFIX/bin" "$HOMEBREW_PREFIX/sbin"
    export HOMEBREW_TEMP="$HOMEBREW_PREFIX/temp"
fi
