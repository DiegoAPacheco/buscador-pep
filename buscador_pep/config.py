import tomllib
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Configuration:
    portal_url: str
    user_profile_path: str

def read_configuration(file_path: Path) -> Configuration:
    with open(file_path, "rb") as f:
        config = tomllib.load(f)
    return Configuration(
        portal_url = config["portal_url"],
        user_profile_path = config["user_profile_path"]
    )
