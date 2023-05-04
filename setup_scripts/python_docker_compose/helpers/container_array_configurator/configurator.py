from helpers.container_array_builder.compose_template import (
    UniversalDockerComposeTemplate,
)
from helpers.container_array_configurator.volume_template import DockerComposeVolume
from helpers.enums.enum_selenium_image import SeleniumImage


class ComposeConfigurator:
    def __init__(self):
        ...

    @classmethod
    def configure(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ):
        # general config
        compose_template = cls._configure_for_local(user_data, compose_template)

        # platform specific config
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
    def _general_config(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ):
        if user_data.get("specify_container_names"):
            for container_base_name, container_user_name in user_data["container_names"].items():
                ...

        if user_data.get("specify_container_ports"):
            for container_base_name, container_user_port in user_data["container_ports"].items():
                ...

        # configure architecture / ??? why
        ...

        if user_data.get("is_arm"):
            compose_template.screenshot_selenium.image = SeleniumImage.ARM
            compose_template.video_gfx_selenium.image = SeleniumImage.ARM

        # configure rebuild Database
        compose_template.env_file['rebuild_db'] = True if user_data.get("rebuild_db") else False
        return compose_template


    @classmethod
    def _configure_for_local(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ):
        # generate local volume
        compose_template.volume = cls._generate_local_volume()

        # 'mount_code_folders': False,
        return compose_template

    @classmethod
    def _configure_for_azure(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ):
        compose_template.volume = cls._generate_azure_volume()
        return compose_template


    @classmethod
    def _configure_for_codespaces(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ):
        return cls._configure_for_local(user_data, compose_template)


    @classmethod
    def _generate_local_volume(cls) -> DockerComposeVolume:
        return DockerComposeVolume(
            name="asset_storage",
            driver= "local",
            driver_type='none',
            driver_o='bind',
            driver_device='$PWD/dev/volume/asset_storage'
        )


    @classmethod
    def _generate_azure_volume(cls) -> DockerComposeVolume:
        return DockerComposeVolume(
            name="asset_storage",
            driver="azure_file",
            driver_type='none',
            driver_o='bind',
            driver_device='$PWD/dev/volume/asset_storage'
        )
