import config
import yaml


def write_to_yaml(output_dict: dict):
    # generate and write docker-compose yaml
    with open(config.DOCKER_COMPOSE_PATH, "wt") as f:
        yaml.dump({"version": output_dict["version"]}, f)
        f.write("\n")
        yaml.dump({"services": output_dict["services"]}, f)
        f.write("\n")

        if output_dict.get("volumes"):
            yaml.dump({"volumes": output_dict["volumes"]}, f)
            f.write("\n")
