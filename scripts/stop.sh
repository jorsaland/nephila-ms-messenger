#!/usr/bin/env bash


set -euo pipefail


cd "$(dirname "$0")/.."


if [[ " ${*} " == *" docker "* ]]; then
    echo "-- Stop MS Messenger from Docker --"
else
    echo "-- Stop MS Messenger process --"
fi


gnome-terminal -- bash -c "sudo ./scripts/helpers/_stop.sh $*"