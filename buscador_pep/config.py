import tomllib
from pathlib import Path
from dataclasses import dataclass

@dataclass
class UserProfile:
    overview: str
    location: str
    industry: str
    job_opening_status: str
    job_category: str
    pay_range: str
    legal_status: str

@dataclass
class Configuration:
    portal_url: str = "https://www.empleospublicos.cl/"
    user_profile: UserProfile

def read_configuration(file_path: Path) -> Configuration:
    with open(file_path, "rb") as f:
        config = tomllib.load(f)
    return Configuration(
        user_profile = UserProfile(**config["user_profile"])
    )
