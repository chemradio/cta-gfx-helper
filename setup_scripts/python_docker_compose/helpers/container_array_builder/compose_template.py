from defaults.default_images import DefaultContainerImages
from defaults.default_names import DefaultContainerNames
from defaults.default_ports import DefaultContainerPorts
from helpers.constants import (
    CONTAINER_LIST,
    CONTAINER_LIST_REQUIRE_DISPATCHER,
    DOCKER_COMPOSE_VERSION,
)
from helpers.container_array_builder.container_template import DockerComposeContainer


class UniversalDockerComposeTemplate:
    def __init__(
        self,
        container_list: list = CONTAINER_LIST,
        default_names=DefaultContainerNames,
        default_ports=DefaultContainerPorts,
        default_images=DefaultContainerImages,
    ):
        self.container_list = container_list
        self.default_names = default_names
        self.default_ports = default_ports
        self.default_images = default_images
        self.env_file = dict()
        self.volumes = list()

        self._populate_container_attributes()
        self._populate_env_file()

    def _populate_container_attributes(self):
        # assign dummy blank objects to container name attributes
        for container_base_name in self.container_list:
            setattr(
                self,
                container_base_name,
                DockerComposeContainer(
                    base_name=container_base_name,
                    name=getattr(self.default_names, container_base_name, None),
                    port=getattr(self.default_ports, container_base_name, None),
                    image=getattr(self.default_images, container_base_name, None),
                ),
            )

    def _populate_env_file(self):
        pass

    def to_docker_compose_dict(self) -> dict:
        output = dict()
        # populate meta
        output["version"] = DOCKER_COMPOSE_VERSION

        # populate containers
        containers_dict = dict()
        for base_name in CONTAINER_LIST:
            containers_dict[base_name] = getattr(self, base_name).to_dict()

        output["services"] = containers_dict

        # populate volumes
        output["volumes"] = {volume.name: volume.to_dict() for volume in self.volumes}

        return output

    def generate_env_dict(self) -> dict:
        output = dict()
        # for base_name in CONTAINER_LIST:
        #     output[f"{base_name}_name"] = getattr(self, base_name).name
        #     output[f"{base_name}_port"] = getattr(self, base_name).port
        return output
