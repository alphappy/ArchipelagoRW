from BaseClasses import MultiWorld
from .classes import LocationData, RoomLocation
from ..conditions import GameStateFlag
from ..game_data.general import scugs_all, scugs_vanilla
from ..options import RainWorldOptions
from ..game_data import static_data
from ..utils import room_effective_whitelist as REW


class Shelter(RoomLocation):
    def __init__(self, room: str, offset: int):
        super().__init__(f"Shelter - {room}", f"Shelter-{room}", [], offset, room)
        self.gamestates = GameStateFlag(0)

    def pre_generate(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        if not options.satisfies(self.gamestates):
            return False
        return super().pre_generate(player, multiworld, options)


def initialize() -> dict[str, Shelter]:
    offset = 5350
    ret: dict[str, Shelter] = {}

    for gameversion, gameversion_data in static_data.items():
        for dlcstate, dlcstate_data in gameversion_data.items():
            for region, region_data in dlcstate_data.items():
                for room, room_data in region_data.items():
                    if "SHELTER" in room_data.get("tags", set()):
                        if (shelter_data := ret.get(room, None)) is None:
                            shelter_data = Shelter(room, offset)
                            ret[room] = shelter_data
                            offset += 1

                        whitelist = REW(room_data, scugs_all if dlcstate == "MSC" else scugs_vanilla)
                        whitelist = whitelist.difference(room_data.get("broken", set()))
                        shelter_data.gamestates[dlcstate, whitelist] = True

    return ret


locations: dict[str, Shelter] = initialize()


def select(options: RainWorldOptions) -> list[LocationData]:
    if options.checks_sheltersanity:
        return list(locations.values())
    return []
