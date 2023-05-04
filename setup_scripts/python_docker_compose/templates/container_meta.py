from dataclasses import dataclass


@dataclass
class DockerComposeContainer:
    build: str
    context: str
    image: str

    env_file: str = ".env"

    name: str
    hostname: str

    port: str
    port_mapping: dict
    expose: bool = False

    volumes: list[dict]
    healthcheck: dict
    depends_on: list | dict = ["dispatcher"]

    privileged: bool | None = None
    shm_size: str | None = "4g"


@dataclass
class DockerComposeVolume:
    name: str
    driver: str
    driver_opts: dict

    driver_type: str
    driver_o: str
    driver_device: str
