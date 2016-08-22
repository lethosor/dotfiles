# add_path VAR begin|end PATH [PATH2...]
function add_path {
    local var="$1"
    if [[ -z "$var" ]]; then
        echo "add_path: missing variable" >/dev/stderr
        return 2
    fi
    shift

    local loc="$1"
    if [[ "$loc" != "begin" ]] && [[ "$loc" != "end" ]]; then
        echo "add_path: location '$loc' not begin|end" >/dev/stderr
        return 2
    fi
    shift

    if [[ -z "$1" ]]; then
        echo "add_path: no paths"
        return 1
    fi

    while [[ "$#" -ne 0 ]]; do
        if [[ ":${!var}" != *":$1:"* ]]; then
            # add path
            if [[ "$loc" = "begin" ]]; then
                export $var="$1:${!var}"
            else
                export $var="${!var}:$1"
            fi
        fi
        shift
    done
}

