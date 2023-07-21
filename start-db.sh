#!/bin/sh

POSTGRES_DATA_DIR="$HOME/.pgdata"

# make data dir if not exits
if [ ! -d "$POSTGRES_DATA_DIR" ]; then
    mkdir "$POSTGRES_DATA_DIR"
fi

# run docker container
docker run \
    --name mypg \
    -p 5432:5432 \
    -e POSTGRES_USER=isaac \
    -e POSTGRES_PASSWORD=112358 \
    -e POSTGRES_DB=test_db \
    -v "$POSTGRES_DATA_DIR":/var/lib/postgresql/data \
    -d \
    postgres
