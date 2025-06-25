from BaseClasses import MultiWorld, Region


def try_get_region(multiworld: MultiWorld, name: str, player: int) -> Region | None:
    try:
        return multiworld.get_region(name, player)
    except KeyError:
        return None
