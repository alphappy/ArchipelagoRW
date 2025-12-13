from BaseClasses import MultiWorld
from ..game_data import static_data
from ..game_data.general import scugs_msc_watcher
from .classes import RoomLocation
from ..options import RainWorldOptions
from ..utils import placed_object_effective_whitelist as POEW

INITIAL_OFFSET = 1200

# Defines karma flowers that only exist after completing the rot ending in Watcher
watcher_endgame_flowers = {
    "WORA_CITY2X", "WORA_CITY10X", "WORA_DESERT4X", "WORA_DESERT8", "WORA_EGG02X"
}

class FlowerLocation(RoomLocation):
    def __init__(self, offset: int, room: str):
        super().__init__(f"Karma Flower - {room}", f"Flower-{room}", ["Flower"], offset, room)
        self.use_whitelist()

    def pre_generate(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        # These flowers being post rot ending means they could only ever be relevant for Spinning Top ending.
        # Needing to complete the rot ending for checks is just... no thanks.
        if self.room in watcher_endgame_flowers:
            return False
        return super().pre_generate(player, multiworld, options)


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
