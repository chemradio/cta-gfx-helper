from helpers.ask_questions import gather_user_data
from helpers.container_array_builder.compose_template import (
    UniversalDockerComposeTemplate,
)


def main():
    # collect user configuration data
    user_data = gather_user_data()

    # generate universal compose template
    universal_template = UniversalDockerComposeTemplate()

    # configure the template with user submitted data

    # generate dict
    ...

    # generate yaml
    ...

    # run docker compose
    ...


if __name__ == "__main__":
    main()
