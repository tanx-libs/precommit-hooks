#!/usr/bin/env python3
import os
import subprocess
import sys

YAMLLINT_CONFIG_FILE = './pre_commit_hooks/config/.yamllint.yaml'

def get_staged_yaml_files():
    # Get the list of staged files using git
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # Filter for YAML files (both .yaml and .yml) and create absolute paths
        # yaml_files = [file for file in result.stdout.splitlines() if file.endswith(('.yml', '.yaml'))]
        yaml_files = [os.path.abspath(file) for file in result.stdout.splitlines() if file.endswith(('.yml', '.yaml'))]
        return yaml_files
    except subprocess.CalledProcessError as e:
        print(f"Error finding staged files: {e.stderr}")
        sys.exit(1)

def check_yamllint_installed():
    # Check if yamllint is installed
    yamllint_path = subprocess.run(
        ['which', 'yamllint'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    ).stdout.strip()
    
    if not yamllint_path:
        print("yamllint could not be found")
        sys.exit(1)
    return yamllint_path

def check_yamllint_config_exists():
    # Check if the Yamllint configuration file exists
    if not os.path.isfile(YAMLLINT_CONFIG_FILE):
        print("Yamllint configuration file not found")
        sys.exit(1)

def lint_yaml_file(yaml_file, yamllint_path):
    # Lint the YAML file using yamllint with the provided config
    try:
        result = subprocess.run(
            [yamllint_path, '-c', YAMLLINT_CONFIG_FILE, yaml_file],  # Include yaml_file at the end
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print(f"Yamllint failed on {yaml_file}")
            print(result.stdout)
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running yamllint on {yaml_file}: {e.stderr}")
        sys.exit(1)

def main():
    # Find staged YAML files
    yaml_files = get_staged_yaml_files()

    # If no YAML files are found, exit successfully
    if not yaml_files:
        sys.exit(0)

    # Check if yamllint is installed
    yamllint_path = check_yamllint_installed()

    # Check if the Yamllint configuration file exists
    check_yamllint_config_exists()

    # Loop through each YAML file and lint it
    for yaml_file in yaml_files:
        lint_yaml_file(yaml_file, yamllint_path)

if __name__ == "__main__":
    main()
