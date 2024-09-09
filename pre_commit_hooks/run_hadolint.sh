#!/bin/bash

# Find all staged Dockerfiles
dockerfiles=$(git diff --cached --name-only --diff-filter=ACM | grep -E 'Dockerfile*')

# Check if no Dockerfiles are found
if [[ -z "$dockerfiles" ]]; then
    echo "No Dockerfiles found in staged changes."
    exit 0
fi

# check if docker is running or not 
if ! command -v docker &> /dev/null
then
    echo "docker could not be found"
    exit 1
fi

# check if hadolint configuration file exists
if [ ! -f ./.hadolint.yaml ]; then
    echo "Hadolint configuration file not found"
    exit 1
fi

# Loop through all staged Dockerfiles and run Hadolint on them
for file in $dockerfiles; do
    # Run Hadolint using the Docker container
    docker run --rm -i -v ./.hadolint.yaml:/.config/hadolint.yaml hadolint/hadolint < "$file"
    if [ $? -ne 0 ]; then
        echo "Hadolint failed on $file"
        exit 1
    fi
done

echo "All Dockerfiles passed Hadolint"