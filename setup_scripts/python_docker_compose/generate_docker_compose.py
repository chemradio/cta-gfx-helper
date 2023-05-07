import config
from helpers.ask_questions import gather_user_data
from helpers.container_array_builder.compose_template import (
    UniversalDockerComposeTemplate,
)
from helpers.container_array_configurator.configurator import ComposeConfigurator
from helpers.dump_yaml import write_to_yaml
from helpers.environment_handler import populate_dict_with_env


def main():
    user_data = gather_user_data()
    compose_template = UniversalDockerComposeTemplate()
    ComposeConfigurator.configure(user_data, compose_template)
    output_dict = compose_template.to_docker_compose_dict()
    write_to_yaml(output_dict)

    env_dict = compose_template.generate_env_dict()

    env_dict = populate_dict_with_env(env_dict)

    with open(config.ENV_FILE_PATH, "wt") as f:
        for key, value in env_dict.items():
            f.write(f"{key}={value}\n")

    if user_data.get("run_after_generation"):
        # run docker compose
        ...

    return


if __name__ == "__main__":
    main()
