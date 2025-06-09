from ..game_data import static_data
from ..game_data.general import scugs_msc_watcher
from .classes import RoomLocation
from ..options import RainWorldOptions
from ..utils import placed_object_effective_whitelist as POEW

INITIAL_OFFSET = 1200


class FlowerLocation(RoomLocation):
    def __init__(self, offset: int, room: str):
        super().__init__(f"Karma Flower - {room}", f"Flower-{room}", [], offset, room)
        self.use_whitelist()


def initialize() -> list[FlowerLocation]:
    ret = {}
    offset = INITIAL_OFFSET

    for gameversion, gameversion_data in static_data.items():
        for dlcstate, dlcstate_data in gameversion_data.items():
            for region, region_data in dlcstate_data.items():
                for room, room_data in region_data.items():
                    if "KarmaFlower" in room_data.get("objects", {}).keys():
                        if ret.get(room, None) is None:
                            ret[room] = FlowerLocation(offset, room)
                            offset += 1

                        whitelist = POEW(room_data, room_data['objects']['KarmaFlower'], set(scugs_msc_watcher))
                        ret[room].whitelist.update(gameversion, dlcstate, whitelist)


    return list(ret.values())


locations = initialize()


def select(options: RainWorldOptions) -> list[FlowerLocation]:
    return locations if options.checks_flowersanity else []
