#!/bin/bash

# Find all staged docker-compose.yml files
compose_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E 'docker-compose.*\.yml')

# Check if no docker-compose files are found
if [[ -z "$compose_files" ]]; then
    # No docker-compose files found, exit without error
    exit 0
fi

# Initialize the flag for docker-compose presence
is_docker_compose_present=0

# Check if docker-compose is installed; if not, check for docker
if ! command -v docker-compose &> /dev/null; then
    if ! command -v docker &> /dev/null; then
        echo "docker-compose or docker is not installed. Please install docker-compose or docker to continue."
        exit 1
    else
        is_docker_compose_present=1
    fi
fi

# Loop through all staged docker-compose.yml files and validate them
for file in $compose_files; do
    # Run docker-compose if it's installed, otherwise use docker compose
    if [ $is_docker_compose_present -eq 0 ]; then
        docker-compose -f "$file" config > /dev/null
    else
        docker compose -f "$file" config > /dev/null
    fi
    
    # Check if the command was successful
    if [ $? -ne 0 ]; then
        echo "Docker Compose validation failed for $file"
        exit 1
    fi
done

# All docker-compose files passed validation
