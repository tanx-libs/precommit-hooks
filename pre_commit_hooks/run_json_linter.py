#!/usr/bin/env python3
import os
import subprocess
import sys

def get_staged_json_files():
    # Get the list of staged files using git
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # Filter for JSON files
        json_files = [file for file in result.stdout.splitlines() if file.endswith('.json')]
        return json_files
    except subprocess.CalledProcessError as e:
        print(f"Error finding staged files: {e.stderr}")
        sys.exit(1)

def check_jq_installed():
    # Check if jq is installed
    if subprocess.call(["which", "jq"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
        print("jq could not be found")
        sys.exit(1)

def lint_json_file(json_file):
    # Lint JSON file using jq
    try:
        result = subprocess.run(
            ['jq', '.', json_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print(f"JSON Linting failed for {json_file}")
            print(result.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error linting {json_file}: {e.stderr}")
        sys.exit(1)

def main():
    # Find staged JSON files
    json_files = get_staged_json_files()

    # If no JSON files are found, exit successfully
    if not json_files:
        sys.exit(0)

    # Check if jq is installed
    check_jq_installed()

    # Loop through each JSON file and lint it
    for json_file in json_files:
        lint_json_file(json_file)

if __name__ == "__main__":
    main()
