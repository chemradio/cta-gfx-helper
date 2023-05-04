from defaults.default_images import DefaultContainerImages
from defaults.default_names import DefaultContainerNames
from defaults.default_ports import DefaultContainerPorts
from helpers.constants import CONTAINER_LIST
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
        self.env_file = {}

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