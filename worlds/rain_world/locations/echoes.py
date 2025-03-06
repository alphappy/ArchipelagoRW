from BaseClasses import MultiWorld
from .classes import LocationData, PhysicalLocation
from ..conditions.classes import Simple, AnyOf
from ..options import RainWorldOptions


class Echo(PhysicalLocation):
    def __init__(self, ghost: str, region: str, offset: int, room: str, free: bool = False):
        super().__init__(f"Echo-{ghost}", f"Echo-{ghost}", region, offset, room)
        self.free = free
        
    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        if not self.free:
            match options.difficulty_echo_low_karma:
                case "never":
                    self.access_condition = Simple("Karma", 4)
                case "with_karma_flower":
                    self.access_condition = AnyOf(Simple("KarmaFlower"), Simple("Karma", 4))
                case "unaltered":
                    if options.starting_scug == "Artificer":
                        self.access_condition = AnyOf(Simple("KarmaFlower"), Simple("Karma", 4))

        return super().make(player, multiworld, options)


# Which echoes are "free" is determined by `GhostWorldPresence.SpawnGhost`.
locations: dict[str, LocationData] = {
    "CC": Echo("CC", "Chimney Canopy", 5070, ""),
    "SH": Echo("SH", "Shaded Citadel", 5071, ""),
    "LF": Echo("LF", "Farm Arrays", 5072, ""),
    "UW": Echo("UW", "The Exterior", 5073, "", True),
    "SI": Echo("SI", "Sky Islands", 5074, ""),
    "SB": Echo("SB", "Subterranean ravine", 5075, "", True),
    "LC": Echo("LC", "Metropolis", 5076, "", True),
    "UG": Echo("UG", "Undergrowth", 5077, ""),
    "CL": Echo("CL", "Silent Construct", 5078, ""),
    "SL": Echo("SL", "Shoreline", 5079, ""),
    "MS": Echo("MS", "Submerged Superstructure", 5080, "", True),
}


def generate(options: RainWorldOptions) -> list[LocationData]:
    match options.starting_scug:
        case "Saint":
            keys = ["CC", "LF", "SI", "SB", "UG", "CL", "SL", "MS"]
        case _:
            # The LC echo does appear for every scug, but the region doesn't populate except for Artificer.
            keys = ["CC", "LF", "SI", "SB", "SH", "UW", "LC"]

    return [locations[key] for key in keys]
