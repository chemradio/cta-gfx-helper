from dataclasses import dataclass, field

DISPATCHER_DEPENDENCY = ["dispatcher"]


@dataclass
class DockerComposeContainer:
    base_name: str
    name: str | None = None
    hostname: str | None = None
    #
    build: str | None = None
    context: str | None = None
    image: str | None = None
    #
    port: str | None = None
    port_mapping: dict | None = None
    volumes: list[dict] | None = None
    #
    expose: bool = False
    env_file: str = ".env"
    depends_on: list | dict | None = None

    healthcheck: dict | None = None
    privileged: bool | None = None
    shm_size: str | None = None

    def __post_init__(self):
        if not self.hostname:
            self.hostname = self.name
