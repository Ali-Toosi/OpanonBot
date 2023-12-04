"""
This script is used to give a dev shell of the chalice app.
Pass "local" after the file name to use .env.local variables as well.
E.g. python src/scripts/start_shell.py local
"""


##################################################
# The file should be run from the root directory #
# python -i src/scripts/...                      #
# Otherwise file access will fail                #
##################################################

import json
import os
import subprocess
import sys


def set_from_env_file(env_file):
    # Check if the env file exists
    if os.path.isfile(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith(";"):
                    # Skip empty lines and comments
                    continue
                key, value = line.split("=", 1)
                os.environ[key] = value

        print(f"Environment variables from {env_file} file have been set.")
    else:
        print(f"Error: The {env_file} file does not exist.")
        raise Exception


def set_from_config_file(stage_name):
    with open("src/.chalice/config.json") as f:
        config = json.loads(f.read())

    for key, val in config.get("environment_variables", {}).items():
        print(f"Setting {key} from config...")
        os.environ[key] = val

    for key, val in (
        config["stages"][stage_name].get("environment_variables", {}).items()
    ):
        print(f"Setting {key} from config...")
        os.environ[key] = val


if __name__ == "__main__":
    """
    Expected command:
    python manage.py <env: either local or stage name> <command: shell | test | run | setup> <extra args for command>
    """
    args = sys.argv[1:]
    stage, command = args[:2]
    extra_args = " ".join(args[2:])

    set_from_config_file(stage)
    set_from_env_file(f"src/.env.{stage}")

    if command == "shell":
        subprocess.call("python -i src/app.py " + extra_args, shell=True)
    if command == "setup":
        return_code = subprocess.call(
            "python src/scripts/setup.py" + extra_args, shell=True
        )
        if return_code != 0:
            # We want the script to fail if setup failed
            exit(return_code)
    elif command == "test":
        os.environ["TESTING"] = "1"
        subprocess.call("pytest src/tests " + extra_args, shell=True)
    elif command == "run":
        if stage != "local":
            print("Can't run locally with non-local config!")
        subprocess.call(
            f"cd src && chalice local --stage {stage} & "
            f"ssh -R {os.environ['SERVEO_SUBDOMAIN']}:80:localhost:8000 serveo.net",
            shell=True,
        )
