#!/usr/bin/env bash


set -euo pipefail


breakpoint() {
    if [[ " ${*} " == *" debug "* ]]; then
        read -rp $'\n=== ENTER to exit ==='
    fi
}
trap 'breakpoint "$@"' EXIT


echo "Stopping Nephila MS Messenger..."


set -o allexport
source .env
set +o allexport


if [[ " ${*} " == *" docker "* ]]; then

    docker stop $APP_NAME || true
    docker rm $APP_NAME || true
    docker rmi $APP_NAME || true

else

    pid_file="./.pid"

    test -f $pid_file \
        && ( kill -2 $(cat $pid_file) 2> /dev/null || true )

fi


echo "Nephila MS Messenger has stopped."