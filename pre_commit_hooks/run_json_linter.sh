#!/bin/bash

# Find all staged JSON files
json_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.json')

# Check if no JSON files are found
if [[ -z "$json_files" ]]; then
    echo "No JSON files found in staged changes."
    exit 0
fi

#  Check if jq is installed
if ! command -v jq &> /dev/null
then
    echo "jq could not be found"
    exit 1
fi

# Loop through all staged JSON files and lint them
for file in $json_files; do
    # RUN Json Linter using jq and redirect the error to a variable
    error=$(jq . "$file" 2>&1 >/dev/null)
    if [ $? -ne 0 ]; then
        echo "JSON Linting failed for $file"
        echo "$error"
        exit 1
    fi
done

echo "All JSON files passed linting"