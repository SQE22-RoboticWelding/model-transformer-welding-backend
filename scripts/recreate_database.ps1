$path = Split-Path $MyInvocation.MyCommand.Path -Parent
$path = Split-Path $path -Parent
$path = "$path\docker-compose.yml"

docker compose --file $path rm -f -s -v sqe_database
docker compose --file $path up -d --no-deps sqe_database
