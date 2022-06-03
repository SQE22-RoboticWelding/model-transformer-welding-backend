#!/usr/bin/env bash

# Get the location path of the script. pwd only returns the location from which the user called the script, but we need
# the exact location of the script to go to the parent folder, which is the root folder of our project with the compose file
path="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

# cd into root path of the backend project
cd "${path}" || exit
cd .. || exit

docker compose rm -f -s -v sqe_database
docker compose up -d --no-deps sqe_database
