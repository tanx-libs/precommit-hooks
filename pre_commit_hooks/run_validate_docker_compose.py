#!/usr/bin/env python3

import subprocess
import sys
import tempfile
import yaml
import os


def get_staged_compose_files():
    # Get the list of staged files using git
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        # Filter for docker-compose.yml files
        compose_files = [
            file
            for file in result.stdout.splitlines()
            if "docker-compose" in file
            and file.endswith(".yml")
            or file.endswith(".yaml")
        ]
        return compose_files
    except subprocess.CalledProcessError as e:
        print(f"Error finding staged files: {e.stderr}")
        sys.exit(1)


def check_docker_compose_installed():
    # Check if docker-compose or docker is installed
    is_docker_compose_installed = (
        subprocess.call(
            ["which", "docker-compose"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        == 0
    )
    is_docker_installed = (
        subprocess.call(
            ["which", "docker"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        == 0
    )

    if not is_docker_compose_installed and not is_docker_installed:
        print(
            "docker-compose or docker is not installed. Please install docker-compose or docker to continue."
        )
        sys.exit(1)

    return is_docker_compose_installed


def remove_dependencies_and_env_files(yaml_content):
    try:
        config = yaml.safe_load(yaml_content)
        for service in config.get("services", {}).values():
            # Remove depends_on
            if "depends_on" in service:
                del service["depends_on"]

            # Remove env_file
            if "env_file" in service:
                del service["env_file"]

            # Remove environment variables that reference .env files
            if "environment" in service:
                service["environment"] = [
                    env
                    for env in service["environment"]
                    if not (isinstance(env, str) and env.startswith("$"))
                ]
                # Remove the environment key if it's empty
                if not service["environment"]:
                    del service["environment"]

        # Remove top-level env_file if it exists
        if "env_file" in config:
            del config["env_file"]

        return yaml.dump(config)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return yaml_content


def validate_compose_file(compose_file, use_docker_compose):
    # Read the original file
    with open(compose_file, "r") as f:
        original_content = f.read()

    # Remove dependencies and env file requirements
    modified_content = remove_dependencies_and_env_files(original_content)

    # Create a temporary file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yml", delete=False
    ) as temp_file:
        temp_file.write(modified_content)
        temp_file_path = temp_file.name

    # Run docker-compose or docker compose to validate the file
    try:
        if use_docker_compose:
            result = subprocess.run(
                ["docker-compose", "-f", temp_file_path, "config"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env={**os.environ, "COMPOSE_IGNORE_ORPHANS": "True"},
            )
        else:
            result = subprocess.run(
                ["docker", "compose", "-f", temp_file_path, "config"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env={**os.environ, "COMPOSE_IGNORE_ORPHANS": "True"},
            )

        # If validation failed
        if result.returncode != 0:
            print(f"Docker Compose validation failed for {compose_file}")
            print(result.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error validating {compose_file}: {e.stderr}")
        sys.exit(1)
    finally:
        # Clean up the temporary file
        subprocess.run(["rm", temp_file_path])


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
