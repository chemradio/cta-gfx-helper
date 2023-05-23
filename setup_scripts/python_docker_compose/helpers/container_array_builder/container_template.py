from dataclasses import asdict, dataclass, field

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
    ports: list[str] | None = field(default_factory=list)  # ports attach to host
    port_mapping: dict | None = None
    volumes: list[str] | None = field(default_factory=list)
    #
    expose: bool = False
    env_file: str = ".env"
    depends_on: list[str] | None = field(default_factory=list)

    healthcheck: dict | None = None
    privileged: bool | None = None
    shm_size: str | None = None

    def __post_init__(self):
        if not self.hostname:
            self.hostname = self.name

    def to_dict(self):
        container_dict = asdict(self)
        return {
            key: value
            for key, value in container_dict.items()
            if (value) and (key not in ("base_name", "name", "port"))
        }
