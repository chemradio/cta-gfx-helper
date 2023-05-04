from templates.container_meta import DockerComposeVolume

local_volume = DockerComposeVolume(
    name="asset_storage",
    driver="local",
    driver_type="none",
    driver_o="bind",
    driver_device="$PWD/dev/volume/asset_storage",
)
