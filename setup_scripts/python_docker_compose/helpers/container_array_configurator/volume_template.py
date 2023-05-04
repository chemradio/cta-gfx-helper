from dataclasses import dataclass


@dataclass
class VolumeOptions:
    type: str | None = None
    o: str | None = None
    device: str | None = None


@dataclass
class DockerComposeVolume:
    name: str
    driver: str

    driver_type: str | None = None
    driver_o: str | None = None
    driver_device: str | None = None

    driver_opts: VolumeOptions | None = None

    def __post_init__(self):
        self.driver_opts = VolumeOptions(
            type=self.driver_type, o=self.driver.o, device=self.driver_device
        )
