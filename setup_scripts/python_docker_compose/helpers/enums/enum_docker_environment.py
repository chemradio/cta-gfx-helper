from enum import Enum


class DockerEnvironment(str, Enum):
    LOCAL = "local"
    AZURE = "azure"
    GITHUB_CODESPACES = "github_codespaces"


class DockerRegistryProvider(str, Enum):
    AZURE = "azure"
    DOCKERHUB = "dockerhub"
