#!/usr/bin/env python3

import subprocess
import sys
import yaml
import os
import re
import tempfile

def get_git_root():
    try:
        git_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], universal_newlines=True
        ).strip()
        return git_root
    except subprocess.CalledProcessError:
        print("Error: This script must be run from within a git repository.")
        sys.exit(1)

def get_staged_compose_files(git_root):
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            cwd=git_root,
        )
        compose_file_pattern = re.compile(r"^docker-compose([-.].*)?\.ya?ml$")
        compose_files = [
            os.path.join(git_root, file)
            for file in result.stdout.splitlines()
            if compose_file_pattern.match(os.path.basename(file))
        ]
        return compose_files
    except subprocess.CalledProcessError as e:
        print(f"Error finding staged files: {e.stderr}")
        sys.exit(1)

def check_docker_compose_installed():
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

    return is_docker_installed  # Prefer 'docker compose' over 'docker-compose'

def remove_dependencies_and_env_files(yaml_content):
    try:
        config = yaml.safe_load(yaml_content)
        for service in config.get("services", {}).values():
            if "depends_on" in service:
                del service["depends_on"]

            if "env_file" in service:
                del service["env_file"]

            if "environment" in service:
                del service["environment"]

            if "networks" in service:
                del service["networks"]

        if "env_file" in config:
            del config["env_file"]

        return yaml.dump(config)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return yaml_content

def validate_compose_file(compose_file, use_docker):
    with open(compose_file, "r") as f:
        original_content = f.read()

    modified_content = remove_dependencies_and_env_files(original_content)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as temp_file:
        temp_file.write(modified_content)
        temp_file_path = temp_file.name

    try:
        if use_docker:
            process = subprocess.run(
                ["docker", "compose", "-f", temp_file_path, "config"],
                capture_output=True,
                text=True,
                check=True,
                env={**os.environ, "COMPOSE_IGNORE_ORPHANS": "True"},
            )
        else:
            process = subprocess.run(
                ["docker-compose", "-f", temp_file_path, "config"],
                capture_output=True,
                text=True,
                check=True,
                env={**os.environ, "COMPOSE_IGNORE_ORPHANS": "True"},
            )
        # check this status 
        if process.returncode != 0:
            print(f"Docker Compose validation failed for {compose_file}")
            print(process.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Docker Compose validation failed for {compose_file}")
        print(e.stderr)
        sys.exit(1)
    finally:
        os.unlink(temp_file_path)

def main():
    git_root = get_git_root()
    compose_files = get_staged_compose_files(git_root)

    if not compose_files:
        print("No Docker Compose files found in staged changes.")
        sys.exit(0)

    use_docker = check_docker_compose_installed()

    for compose_file in compose_files:
        validate_compose_file(compose_file, use_docker)

if __name__ == "__main__":
    main()