import tomllib
from pathlib import Path
from dataclasses import dataclass

@dataclass
class UserProfileFilters:
    location: str
    industry: str
    job_opening_status: str
    job_category: str
    pay_range: str
    legal_status: str

@dataclass
class UserProfile:
    overview: str
    filters: UserProfileFilters

@dataclass
class Configuration:
    user_profile: UserProfile
    portal_url: str = "https://www.empleospublicos.cl/"

def read_configuration(file_path: Path) -> Configuration:
    with open(file_path, "rb") as f:
        config = tomllib.load(f)
    user_profile = config["user_profile"]

    if not isinstance(user_profile, dict):
        raise KeyError("Missing 'user_profile' key in configuration file")

    if isinstance(user_profile.get("filters"), dict):
        user_profile["filters"] = UserProfileFilters(**user_profile["filters"])
    return Configuration(
        user_profile=UserProfile(**user_profile)
    )
