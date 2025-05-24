from BaseClasses import MultiWorld
from .classes import LocationData, RoomLocation
from ..conditions.classes import Simple, AnyOf
from ..options import RainWorldOptions


class Echo(RoomLocation):
    def __init__(self, ghost: str, offset: int, room: str, free: bool = False):
        super().__init__("Echo", f"Echo-{ghost}", [], offset, room)
        self.free = free
        
    def pre_generate(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        if not self.free:
            match options.difficulty_echo_low_karma:
                case "never":
                    self.access_condition = Simple("Karma", 4)
                case "with_karma_flower":
                    self.access_condition = AnyOf(Simple("KarmaFlower"), Simple("Karma", 4))
                case "unaltered":
                    if options.starting_scug == "Artificer":
                        self.access_condition = AnyOf(Simple("KarmaFlower"), Simple("Karma", 4))

        return super().pre_generate(player, multiworld, options)


# Which echoes are "free" is determined by `GhostWorldPresence.SpawnGhost`.
locations: dict[str, LocationData] = {
    "CC": Echo("CC", 5070, "CC_C12"),
    "SH": Echo("SH", 5071, "SH_A08"),
    "LF": Echo("LF", 5072, "LF_B01"),
    "UW": Echo("UW", 5073, "UW_A14", True),
    "SI": Echo("SI", 5074, "SI_B11"),
    "SB": Echo("SB", 5075, "SB_A10", True),
    "LC": Echo("LC", 5076, "LC_HIGHESTPOINT", True),
    "UG": Echo("UG", 5077, "UG_C02"),
    "CL": Echo("CL", 5078, "CL_D05"),
    "SL": Echo("SL", 5079, "SL_WALL06"),
    "MS": Echo("MS", 5080, "MS_COMMS", True),
}


def generate(options: RainWorldOptions) -> list[LocationData]:
    match options.starting_scug:
        case "Saint":
            keys = ["CC", "LF", "SI", "SB", "UG", "CL", "SL", "MS"]
        case "Watcher":
            return []
        case _:
            # The LC echo does appear for every scug, but the region doesn't populate except for Artificer.
            keys = ["CC", "LF", "SI", "SB", "SH", "UW", "LC"]

    return [locations[key] for key in keys]
