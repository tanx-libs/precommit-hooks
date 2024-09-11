#!/usr/bin/env python3
import subprocess
import sys

def get_staged_compose_files():
    # Get the list of staged files using git
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # Filter for docker-compose.yml files
        compose_files = [file for file in result.stdout.splitlines() if 'docker-compose' in file and file.endswith('.yml')]
        return compose_files
    except subprocess.CalledProcessError as e:
        print(f"Error finding staged files: {e.stderr}")
        sys.exit(1)

def check_docker_compose_installed():
    # Check if docker-compose or docker is installed
    is_docker_compose_installed = subprocess.call(
        ["which", "docker-compose"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) == 0
    is_docker_installed = subprocess.call(
        ["which", "docker"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) == 0

    if not is_docker_compose_installed and not is_docker_installed:
        print("docker-compose or docker is not installed. Please install docker-compose or docker to continue.")
        sys.exit(1)
    
    return is_docker_compose_installed

def validate_compose_file(compose_file, use_docker_compose):
    # Run docker-compose or docker compose to validate the file
    try:
        if use_docker_compose:
            result = subprocess.run(
                ['docker-compose', '-f', compose_file, 'config'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        else:
            result = subprocess.run(
                ['docker', 'compose', '-f', compose_file, 'config'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        # If validation failed
        if result.returncode != 0:
            print(f"Docker Compose validation failed for {compose_file}")
            print(result.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error validating {compose_file}: {e.stderr}")
        sys.exit(1)

def main():
    # Get the list of staged docker-compose files
    compose_files = get_staged_compose_files()

    # If no docker-compose files are found, exit successfully
    if not compose_files:
        sys.exit(0)

    # Check if docker-compose or docker is installed
    use_docker_compose = check_docker_compose_installed()

    # Validate each docker-compose file
    for compose_file in compose_files:
        validate_compose_file(compose_file, use_docker_compose)

if __name__ == "__main__":
    main()
