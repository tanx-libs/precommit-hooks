#!/usr/bin/env python3
import os
import subprocess
import sys

def get_staged_dockerfiles():
    # Get the list of staged files using git
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # Filter for Dockerfiles
        dockerfiles = [file for file in result.stdout.splitlines() if 'Dockerfile' in file]
        return dockerfiles
    except subprocess.CalledProcessError as e:
        print(f"Error finding staged files: {e.stderr}")
        sys.exit(1)

def check_docker_installed():
    # Check if Docker is installed
    if subprocess.call(["which", "docker"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
        print("docker could not be found")
        sys.exit(1)

def check_hadolint_config_exists():
    # Check if the Hadolint configuration file exists
    if not os.path.isfile('./.hadolint.yaml'):
        print("Hadolint configuration file not found")
        sys.exit(1)

def run_hadolint_on_dockerfile(dockerfile):
    # Run Hadolint on the Dockerfile
    try:
        with open(dockerfile, 'r') as f:
            result = subprocess.run(
                ['docker', 'run', '--rm', '-i', '-v', './config/.hadolint.yaml:/.config/hadolint.yaml', 'hadolint/hadolint'],
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        if result.returncode != 0:
            print(f"Hadolint failed on {dockerfile}")
            print(result.stdout)
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running Hadolint on {dockerfile}: {e.stderr}")
        sys.exit(1)

def main():
    # Find staged Dockerfiles
    dockerfiles = get_staged_dockerfiles()

    # If no Dockerfiles are found, exit successfully
    if not dockerfiles:
        sys.exit(0)

    # Check if Docker is installed
    check_docker_installed()

    # Check if the Hadolint configuration file exists
    check_hadolint_config_exists()

    # Loop through each Dockerfile and run Hadolint
    for dockerfile in dockerfiles:
        run_hadolint_on_dockerfile(dockerfile)

if __name__ == "__main__":
    main()
