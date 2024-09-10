#!/bin/bash

# Find all staged docker-compose.yml files
compose_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E 'docker-compose.*\.yml')

# Check if no docker-compose files are found
if [[ -z "$compose_files" ]]; then
    # echo "No docker-compose.yml files found in staged changes."
    exit 0
fi

# check if docker-compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "docker-compose could not be found"
    exit 1
fi

# Loop through all staged docker-compose.yml files and validate them
for file in $compose_files; do
    # Run Docker Compose config validation
    docker-compose -f "$file" config --quiet
    if [ $? -ne 0 ]; then
        echo "Docker Compose validation failed for $file"
        exit 1
    fi
done

# echo "All docker-compose.yml files passed validation"
