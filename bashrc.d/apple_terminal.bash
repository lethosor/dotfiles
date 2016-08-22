if [ "$TERM_PROGRAM" = "Apple_Terminal" ]; then
    # Needed so directories in window title bar still work after 'exec bash'
    update_terminal_cwd () {
        local SEARCH=' ';
        local REPLACE='%20';
        local PWD_URL="file://$HOSTNAME${PWD//$SEARCH/$REPLACE}";
        printf '\e]7;%s\a' "$PWD_URL"
    }
    export PROMPT_COMMAND="update_terminal_cwd; $PROMPT_COMMAND"
fi
