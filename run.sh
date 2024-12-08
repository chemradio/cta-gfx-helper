#!/bin/bash

# Run the copy_libs.sh script
./scripts/copy_libs.sh

# Start Docker Compose services
cd compose_containers
docker compose down
docker compose up --build