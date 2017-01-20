if [ -n "$HOMEBREW_PREFIX" ]; then
    add_path PATH begin "$HOMEBREW_PREFIX/bin" "$HOMEBREW_PREFIX/sbin"
fi
