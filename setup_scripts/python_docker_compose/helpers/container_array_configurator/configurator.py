from helpers.constants import (
    CONTAINER_LIST_DEV_FOLDERS,
    CONTAINER_LIST_REQUIRE_VOLUME_MOUNT,
)
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
        cls._general_config(user_data, compose_template)

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
    ) -> None:
        if user_data.get("specify_container_names"):
            for container_base_name, container_user_name in user_data[
                "container_names"
            ].items():
                container = getattr(compose_template, container_base_name)
                container.name = container_user_name
                container.hostname = container_user_name

        if user_data.get("specify_container_ports"):
            for container_base_name, container_user_port in user_data[
                "container_ports"
            ].items():
                container = getattr(compose_template, container_base_name)
                container.port = container_user_port

        # is Arm
        if user_data.get("is_arm"):
            compose_template.screenshot_selenium.image = SeleniumImage.ARM.value
            compose_template.video_gfx_selenium.image = SeleniumImage.ARM.value
        else:
            compose_template.screenshot_selenium.image = SeleniumImage.NORMAL.value
            compose_template.video_gfx_selenium.image = SeleniumImage.NORMAL.value

        # configure rebuild Database
        compose_template.env_file["rebuild_db"] = (
            True if user_data.get("rebuild_db") else False
        )

    @classmethod
    def _configure_for_local(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ) -> None:
        volume = cls._generate_local_volume()
        compose_template.volumes.append(volume)
        cls._assign_storage_volume_to_containers(volume, compose_template)

        # mount code folders
        if user_data.get("mount_code_folders"):
            cls._assign_dev_volume_to_containers(compose_template)

        return compose_template

    @classmethod
    def _configure_for_azure(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ) -> None:
        volume = cls._generate_azure_volume()
        compose_template.volumes.append(volume)
        cls._assign_storage_volume_to_containers(volume, compose_template)

    @classmethod
    def _configure_for_codespaces(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ) -> None:
        cls._configure_for_local(user_data, compose_template)

    @classmethod
    def _generate_local_volume(cls) -> DockerComposeVolume:
        return DockerComposeVolume(
            name="asset_storage",
            driver="local",
            driver_type="none",
            driver_o="bind",
            driver_device="$PWD/dev/volume/asset_storage",
        )

    @classmethod
    def _generate_azure_volume(cls) -> DockerComposeVolume:
        return DockerComposeVolume(
            name="asset_storage",
            driver="azure_file",
            driver_type="none",
            driver_o="bind",
            driver_device="$PWD/dev/volume/asset_storage",
        )

    @classmethod
    def _assign_storage_volume_to_containers(
        cls,
        volume: DockerComposeVolume,
        compose_template: UniversalDockerComposeTemplate,
    ) -> None:
        for base_name in CONTAINER_LIST_REQUIRE_VOLUME_MOUNT:
            container = getattr(compose_template, base_name)
            container.volumes.append(f"{volume.name}:/usr/src/app/volume")

    @classmethod
    def _assign_dev_volume_to_containers(
        cls,
        compose_template: UniversalDockerComposeTemplate,
    ) -> None:
        for base_name, dev_folder in CONTAINER_LIST_DEV_FOLDERS.items():
            container = getattr(compose_template, base_name)
            container.volumes.append(f"{dev_folder}:/usr/src/app")
