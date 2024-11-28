from dataclasses import dataclass

from .domain_enum import DomainName


@dataclass
class LinkParse:
    clean_url: str
    domain: DomainName
    two_layer: bool
