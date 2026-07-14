#!/usr/bin/env bash


set -euo pipefail


cd "$(dirname "$0")/.."


if [[ " ${*} " == *" docker "* ]]; then
    echo "-- Start MS Messenger with Docker --"
else
    echo "-- Start MS Messenger process --"
fi


gnome-terminal -- bash -c "sudo ./scripts/helpers/_start.sh $*"