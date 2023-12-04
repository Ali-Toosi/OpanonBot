"""
This script is used to inject env vars from .env to .chalice/config.json before deployment.
This is used to separate the env vars that can be stored on Git and those that can't (secrets).
"""


##################################################
# The file should be run from the root directory #
# python -i src/scripts/...                      #
# Otherwise file access will fail                #
##################################################

import json


def read_env_file(stage_name):
    res = {}
    with open(f"src/.env.{stage_name}") as f:
        for line in f.read().split("\n"):
            line = line.strip()
            if line == "" or line.startswith("#") or line.startswith(";"):
                continue
            res[line.split("=")[0]] = "=".join(line.split("=")[1:])

    return res


def read_config_file():
    with open("src/.chalice/config.json") as f:
        return json.loads(f.read())


def write_config_file(content: dict):
    with open("src/.chalice/config.json", "w") as f:
        f.write(json.dumps(content, indent=2))


def inject_stage_env_vars():
    config_file = read_config_file()
    stage_names = config_file["stages"].keys()

    for stage in stage_names:
        new_vars = read_env_file(stage)
        config_file["stages"][stage]["environment_variables"].update(new_vars)

    write_config_file(config_file)


if __name__ == "__main__":
    inject_stage_env_vars()
