#!/bin/sh

# Exit when any command fails
set -e

# Pull Qdrant image if it does not exists

QDRANT_IMAGE_URL="qdrant/qdrant"

if ! docker images --quiet $QDRANT_IMAGE_URL > /dev/null 2>&1; then
    echo "Qdrant image does not exist"
    echo "Pulling Qdrant from docker hub..."
    docker pull "$QDRANT_IMAGE_URL"
fi

# Container name
QDRANT_CONTAINER_NAME="myqdrant"

# Dir storing Qdrant data
QDRANT_DATA_DIR="$HOME/.qdrant-data"

# Make data dir if not exits
if [ ! -d "$QDRANT_DATA_DIR" ]; then
    mkdir "$QDRANT_DATA_DIR"
fi

# run docker container
docker run \
    --rm \
    --name $QDRANT_CONTAINER_NAME \
    -p 6333:6333 \
    -v "$QDRANT_DATA_DIR":/qdrant/storage \
    -d \
    qdrant/qdrant
