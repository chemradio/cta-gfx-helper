from helpers.ask_questions import gather_user_data
from helpers.container_array_builder.compose_template import (
    UniversalDockerComposeTemplate,
)
from helpers.container_array_configurator.configurator import ComposeConfigurator

def main():
    # collect user configuration data
    user_data = gather_user_data()
    from pprint import pprint
    pprint(user_data)
    return 
    # generate universal compose template
    compose_template = UniversalDockerComposeTemplate()

    # configure the template with user submitted data
    ComposeConfigurator.configure(user_data, compose_template)

    # generate dict
    ...

    # generate yaml
    ...


    if user_data.get('run_after_generation'):
        # run docker compose



if __name__ == "__main__":
    main()
