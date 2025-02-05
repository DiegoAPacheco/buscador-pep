from pathlib import Path
from dataclasses import dataclass

@dataclass
class UserProfile:
    profile: str


def read_user_profile(file_path: Path) -> UserProfile:
    with open(file_path, "r", encoding="utf-8") as f:
        profile_text = f.read().strip()
    return UserProfile(profile=profile_text)