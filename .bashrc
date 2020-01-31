# Load _* scripts first
. ~/bashrc.d/_funcs.bash
. ~/bashrc.d/_paths.bash
. ~/bashrc.d/_vars.bash

for script in $(find ~/bashrc.d/local/ -name '_*.bash'); do
    . "$script"
done

for script in ~/bashrc.d/*.bash; do
    if [[ "$(basename "$script")" != "_"* ]]; then
        . "$script"
    fi
done

for script in $(find ~/bashrc.d/local/ -name '*.bash'); do
    if [[ "$(basename "$script")" != "_"* ]]; then
        . "$script"
    fi
done

for script in $(echo "$BASHRC_EXTRA" | tr ':' '\n'); do
    . "$script"
done
