. ~/bashrc.d/_funcs.bash
. ~/bashrc.d/_paths.bash

if [ -z "$bash_profile_loaded" ]
then
    uptime
    if cmd_exists fortune && cmd_exists cowsay; then
        . ~/bashrc.d/profile/cows.bash
    fi
    export bash_profile_loaded=1
fi
