. ~/bashrc.d/_funcs.bash
. ~/bashrc.d/_paths.bash

if [ -z "$bash_profile_loaded" ]
then
    if [ -t 0 ] && [ -t 1 ] && [ -t 2 ]; then
        uptime
        if cmd_exists fortune && cmd_exists cowsay; then
            . ~/bashrc.d/profile/cows.bash
        fi
    fi
    export bash_profile_loaded=1
fi
