from helpers.container_array_builder.compose_template import (
    UniversalDockerComposeTemplate,
)


class ComposeConfigurator:
    def __init__(self):
        ...

    @classmethod
    def configure(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ):
        match user_data.get("platform"):
            case "local":
                return cls._configure_for_local(user_data, compose_template)
            case "azure":
                return cls._configure_for_azure(user_data, compose_template)
            case "codespaces":
                return cls._configure_for_codespaces(user_data, compose_template)
            case _:
                return None

    @classmethod
    def _configure_for_azure(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ):
        ...

    @classmethod
    def _configure_for_local(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ):
        ...

    @classmethod
    def _configure_for_codespaces(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ):
        return cls._configure_for_local(user_data, compose_template)
