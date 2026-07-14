#!/usr/bin/env bash


set -euo pipefail


breakpoint() {
    if [[ " ${*} " == *" debug "* ]]; then
        read -rp $'\n=== ENTER to exit ==='
    fi
}
trap 'breakpoint "$@"' EXIT


echo $'\n=== Nephila MS Messenger ===\n'


set -o allexport
source .env
set +o allexport


if [[ " ${*} " == *" docker "* ]]; then

    ./scripts/helpers/_stop.sh docker
    echo "Starting Nephila MS Messenger..."

    logs_dir="./logs"
    [[ -d $logs_dir ]] || mkdir -p $logs_dir

    docker build -f Dockerfile.g -t $APP_NAME .
    docker run \
        --publish 127.0.0.1:$PORT:$PORT \
        --env-file .env \
        --env RUN_MODE=docker \
        --name $APP_NAME \
        --mount type=bind,src=$PWD/logs,target=/usr/src/logs \
        --detach \
        $APP_NAME

else

    ./scripts/helpers/_stop.sh
    echo "Starting Nephila MS Messenger..."

    source ./env/bin/activate
    gunicorn "app.builder:build_app()"

fi