from .classes import LocationData, RoomLocation
from ..game_data.general import scugs_msc_watcher
from ..options import RainWorldOptions
from ..game_data import static_data
from ..utils import room_effective_whitelist as REW


class Shelter(RoomLocation):
    def __init__(self, room: str, offset: int):
        super().__init__(f"Shelter - {room}", f"Shelter-{room}", [], offset, room)
        self.use_whitelist()


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

                        whitelist = REW(room_data, scugs_msc_watcher)
                        whitelist = whitelist.difference(room_data.get("broken", set()))
                        shelter_data.whitelist.update(gameversion, dlcstate, whitelist)

    return ret


locations: dict[str, Shelter] = initialize()


def select(options: RainWorldOptions) -> list[LocationData]:
    if options.checks_sheltersanity:
        return list(locations.values())
    return []
