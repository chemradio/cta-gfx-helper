from helpers.constants import (
    CONTAINER_LIST_BUILD_DEV_FOLDERS,
    CONTAINER_LIST_REQUIRE_CUSTOM_REMOTE_IMAGE,
    CONTAINER_LIST_REQUIRE_VOLUME_MOUNT,
)
from helpers.container_array_builder.compose_template import (
    UniversalDockerComposeTemplate,
)
from helpers.container_array_builder.container_template import DockerComposeContainer
from helpers.container_array_configurator.volume_template import DockerComposeVolume
from helpers.enums.enum_docker_environment import DockerRegistryProvider
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

        # configure selenium containers
        selenium_containers = ["screenshot_selenium", "video_gfx_selenium"]
        for selenium_container in selenium_containers:
            container: DockerComposeContainer = getattr(
                compose_template, selenium_container
            )
            container.shm_size = "4g"
            container.privileged = True

        # intercontainer dependencies
        dispatcher_dependents = [
            "front_svelte",
            "telegram_bot",
            "telegram_sender",
            "screenshoter",
            "video_gfx",
            "video_gfx_server",
            "screenshot_selenium",
            "video_gfx_selenium",
        ]
        for container in dispatcher_dependents:
            container: DockerComposeContainer = getattr(compose_template, container)
            container.depends_on.append("dispatcher")

        dispatcher_container: DockerComposeContainer = getattr(
            compose_template, "dispatcher"
        )
        dispatcher_container.depends_on.append("db")

        # configure rebuild Database
        compose_template.env_file["rebuild_db"] = (
            True if user_data.get("rebuild_db") else False
        )

        # provide build context for containers without predefined images
        cls._assing_build_folders_to_containers(compose_template)

    @classmethod
    def _configure_for_local(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ) -> None:
        volume = cls._generate_local_volume()
        compose_template.volumes.append(volume)
        cls._assign_storage_volume_to_containers(volume, compose_template)
        cls._assign_remote_images_to_containers(user_data, compose_template)

        # mount code folders
        if user_data.get("mount_code_folders"):
            cls._assign_dev_volume_to_containers(compose_template)

        # expose ports
        dispatcher_container = getattr(compose_template, "dispatcher")
        dispatcher_container.ports = [
            f"{dispatcher_container.port}:{dispatcher_container.port}",
        ]

        front_svelte_container = getattr(compose_template, "front_svelte")
        front_svelte_container.ports = [
            f"{front_svelte_container.port}:{front_svelte_container.port}",
        ]
        return compose_template

    @classmethod
    def _configure_for_azure(
        cls, user_data: dict, compose_template: UniversalDockerComposeTemplate
    ) -> None:
        volume = cls._generate_azure_volume()
        compose_template.volumes.append(volume)
        cls._assign_storage_volume_to_containers(volume, compose_template)
        cls._assign_remote_images_to_containers(user_data, compose_template)

        # expose ports
        front_svelte_container = getattr(compose_template, "front_svelte")
        front_svelte_container.ports = [
            f"80:{front_svelte_container.port}",
        ]

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
        """Attach a local folder for watching file generation in the container.
        Only for local development purposes."""
        for base_name, dev_folder in CONTAINER_LIST_BUILD_DEV_FOLDERS.items():
            container = getattr(compose_template, base_name)
            container.volumes.append(f"{dev_folder}:/usr/src/app")

    @classmethod
    def _assing_build_folders_to_containers(
        cls,
        compose_template: UniversalDockerComposeTemplate,
    ) -> None:
        """Assign Build folders for container building and possible attachment
        of container's code folders to local dev folders for hot reload on code changes.
        """
        for base_name, build_folder in CONTAINER_LIST_BUILD_DEV_FOLDERS.items():
            container = getattr(compose_template, base_name)
            container.build = build_folder
            # container.volumes.append(f"{dev_folder}:/usr/src/app")

    @classmethod
    def _assign_remote_images_to_containers(
        cls,
        user_data: dict,
        compose_template: UniversalDockerComposeTemplate,
    ) -> None:
        """Assign remote images to containers. Images are stored in a remote registry like AzureCR."""
        registry_prefix: str = user_data.get("registry_prefix")
        registry_provider: str = user_data.get("registry_provider")
        for base_name in CONTAINER_LIST_REQUIRE_CUSTOM_REMOTE_IMAGE:
            container = getattr(compose_template, base_name)
            if registry_provider == DockerRegistryProvider.AZURE:
                image_string = f"{registry_prefix}.azurecr.io/{base_name}"

            elif registry_provider == DockerRegistryProvider.DOCKERHUB:
                image_string = f"{registry_prefix}:{base_name}"

            container.image = image_string
