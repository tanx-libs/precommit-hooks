#!/bin/bash

# Find all staged YAML files
yaml_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '.*\.ya?ml$')

yamllint_path=$(which yamllint)

yamllint_config_file=".yamllint.yaml"

# Check if no YAML files are found
if [[ -z "$yaml_files" ]]; then
    # echo "No YAML files found in staged changes."
    exit 0
fi

# Check if yamllint is installed
if ! command -v $yamllint_path &> /dev/null
then
    echo "yamllint could not be found"
    exit 1
fi

# check if yamllint configuration file exists
if [ ! -f $yamllint_config_file ]; then
    echo "Yamllint configuration file not found"
    exit 1
fi

# Loop through all staged YAML files and run yamllint on them
for file in $yaml_files; do
    # Run yamllint using the Docker container
    # check if yamllint is installed
    $yamllint_path -c $yamllint_config_file "$file"
    if [ $? -ne 0 ]; then
        echo "Yamllint failed on $file"
        exit 1
    fi
done

# echo "All YAML files passed Yamllint"