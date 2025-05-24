from ..game_data import static_data
from .classes import RoomLocation
from ..options import RainWorldOptions

INITIAL_OFFSET = 1200


class FlowerLocation(RoomLocation):
    def __init__(self, offset: int, room: str):
        super().__init__(f"Karma Flower - {room}", f"Karma Flower - {room}", [], offset, room)


def initialize() -> list[FlowerLocation]:
    ret = []
    offset = INITIAL_OFFSET

    for region, region_data in static_data["1.10.4"]["MSC_Watcher"].items():
        for room, room_data in region_data.items():
            if "KarmaFlower" in room_data.get("objects", {}).keys():
                ret.append(FlowerLocation(offset, room))
                offset += 1

    return ret


locations = initialize()


def select(options: RainWorldOptions) -> list[FlowerLocation]:
    return locations if options.checks_karma_flowers else []
