# Load _* scripts first
. ~/bashrc.d/_funcs.bash
. ~/bashrc.d/_paths.bash
. ~/bashrc.d/_vars.bash

for script in ~/bashrc.d/*.bash; do
    if [[ "$(basename "$script")" != "_"* ]]; then
        . "$script"
    fi
done

for script in $(find ~/bashrc.d/local/ -name '*.bash'); do
    . "$script"
done
