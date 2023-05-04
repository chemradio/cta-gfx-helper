import inquirer

from helpers.enums.enum_docker_environment import DockerEnvironment


def gather_user_data() -> dict:
    """Ask user a series of questions to collect all user specific data required for the app setup"""
    output = dict()

    # select environment
    print("\033c", end="")
    platform = inquirer.prompt(
        [
            inquirer.List(
                "platform",
                "Please select your platform",
                [
                    DockerEnvironment.LOCAL,
                    DockerEnvironment.AZURE,
                    DockerEnvironment.GITHUB_CODESPACES,
                ],
            ),
        ]
    )
    output.update(platform)

    # rebuild db
    print("\033c", end="")
    rebuild_db = inquirer.prompt(
        [
            inquirer.List(
                "rebuild_db",
                "Erase and rebuild the DB?",
                [
                    True,
                    False,
                ],
            ),
        ]
    )
    output.update(rebuild_db)
    print("\033c", end="")

    # mount code folders
    mount_code_folders = (
        inquirer.prompt(
            [
                inquirer.List(
                    "mount_code_folders",
                    "Should we mount the source code folders to docker for debugging",
                    [True, False],
                )
            ]
        )
        if platform["platform"] == "local"
        else {"mount_code_folders": False}
    )
    output.update(mount_code_folders)

    # specify container names
    print("\033c", end="")
    specify_container_names = inquirer.prompt(
        [
            inquirer.List(
                "specify_container_names",
                "Do you want to give containers different names?",
                [True, False],
            )
        ]
    )["specify_container_names"]
    if specify_container_names:
        output.update({"specify_container_names": True})

        container_names = inquirer.prompt(
            [
                inquirer.Text(
                    "dispatcher",
                    "Container name: the Dispatcher - Python/FastAPI",
                    "dispatcher",
                ),
                inquirer.Text(
                    "front_svelte",
                    "Container name: the SvelteKit frontend website",
                    "front_svelte",
                ),
                inquirer.Text(
                    "telegram_bot",
                    "Container name: the Telegram frontend bot",
                    "telegram_bot",
                ),
                inquirer.Text(
                    "db", "Container name: the Postgres database container", "db"
                ),
                inquirer.Text(
                    "screenshoter",
                    "Container name: the Screenshoter engine",
                    "screenshoter",
                ),
                inquirer.Text(
                    "video_gfx", "Container name: the VideoGFX engine", "video_gfx"
                ),
                inquirer.Text(
                    "video_gfx_server",
                    "Container name: the VideoGFX Server container",
                    "video_gfx_server",
                ),
                inquirer.Text(
                    "sender",
                    "Container name: the Telegram ready order sender engine",
                    "sender",
                ),
                inquirer.Text(
                    "screenshot_selenium",
                    "Utility: Selenium grid node for Screenshot engine",
                    "screenshot_selenium",
                ),
                inquirer.Text(
                    "video_gfx_selenium",
                    "Utility: Selenium grid node for VideoGFX engine",
                    "video_gfx_selenium",
                ),
            ]
        )
        output.update({"container_names": container_names})
    else:
        output.update({"specify_container_names": False})

    # specify container ports
    print("\033c", end="")
    specify_container_ports = inquirer.prompt(
        [
            inquirer.List(
                "specify_container_ports",
                "Do you want to assign different port numbers to containers?",
                [True, False],
            )
        ]
    )["specify_container_ports"]
    if specify_container_ports:
        output.update({"specify_container_ports": True})
        container_ports = inquirer.prompt(
            [
                inquirer.Text(
                    "dispatcher",
                    "Container port: the Dispatcher - Python/FastAPI",
                    9000,
                ),
                inquirer.Text(
                    "front_svelte",
                    "Container port: the SvelteKit frontend website",
                    9009,
                ),
                inquirer.Text(
                    "telegram_bot",
                    "Container port: the Telegram frontend bot",
                    9001,
                ),
                inquirer.Text(
                    "screenshoter",
                    "Container port: the Screenshoter engine",
                    9002,
                ),
                inquirer.Text("video_gfx", "Container port: the VideoGFX engine", 9004),
                inquirer.Text(
                    "video_gfx_server",
                    "Container port: the VideoGFX Server container",
                    9006,
                ),
                inquirer.Text(
                    "sender",
                    "Container port: the Telegram ready order sender engine",
                    9007,
                ),
            ]
        )
        output.update({"container_ports": container_ports})
    else:
        output.update({"specify_container_ports": False})

    # check architecture ARM or not
    print("\033c", end="")
    is_arm = inquirer.prompt(
        [
            inquirer.List(
                "is_arm",
                "Are you running ARM architecture?",
                [True, False],
            )
        ]
    )
    output.update(is_arm)

    # run after generation
    print("\033c", end="")
    run_after_generation = inquirer.prompt(
        [
            inquirer.List(
                "run_after_generation",
                "Should Docker-Compose run after generation?",
                [True, False],
            )
        ]
    )
    output.update(run_after_generation)

    return output


if __name__ == "__main__":
    from pprint import pprint

    pprint(gather_user_data())
