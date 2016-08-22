echo bashrc

# Load _* scripts first
. ~/bashrc.d/_funcs.bash
. ~/bashrc.d/_paths.bash
. ~/bashrc.d/_vars.bash

for script in ~/bashrc.d/*.bash; do
    if [[ "$(basename "$script")" != "_"* ]]; then
        echo '>' $script
        . "$script"
    fi
done
