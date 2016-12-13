if [ "$TERM_PROGRAM" = "Apple_Terminal" ]; then
    # Needed so directories in window title bar still work after 'exec bash'

    osver=$(uname -r | cut -d. -f1)
    if [ "$osver" -ge 15 ]; then
        update_terminal_cwd () {
            local url_path='';
            {
                local i ch hexch LC_CTYPE=C LC_ALL=;
                for ((i = 0; i < ${#PWD}; ++i))
                do
                    ch="${PWD:i:1}";
                    if [[ "$ch" =~ [/._~A-Za-z0-9-] ]]; then
                        url_path+="$ch";
                    else
                        printf -v hexch "%02X" "'$ch";
                        url_path+="%${hexch: -2:2}";
                    fi;
                done
            };
            printf '\e]7;%s\a' "file://$HOSTNAME$url_path"
        }
    else
        update_terminal_cwd () {
            local SEARCH=' ';
            local REPLACE='%20';
            local PWD_URL="file://$HOSTNAME${PWD//$SEARCH/$REPLACE}";
            printf '\e]7;%s\a' "$PWD_URL"
        }
    fi
    unset osver

    export PROMPT_COMMAND="update_terminal_cwd; $PROMPT_COMMAND"
fi
