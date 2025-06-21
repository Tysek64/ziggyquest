
from pathlib import Path
from src.backend.Character import Character
from src.backend.CharacterParser import CharacterFactory

def load_characters(character_root_path: Path, tiers: list[str] | None = None) -> tuple[list[list[Character]], list[str]]:
    factory = CharacterFactory()
    character_tier_list = []
    if tiers is None:
        tiers = [tier.name for tier in character_root_path.iterdir() if tier.is_dir()]

    for tier in tiers:
        character_tier_list.append(factory.make_characters(character_root_path / tier))

    return character_tier_list, tiers