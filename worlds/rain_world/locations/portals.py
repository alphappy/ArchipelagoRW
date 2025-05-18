from BaseClasses import MultiWorld
from .classes import LocationData, RoomLocation
from ..conditions import GameStateFlag
from ..game_data.general import scugs_all, scugs_vanilla
from ..options import RainWorldOptions
from ..game_data import static_data, general
from ..game_data.watcher import portals, PortalData

INITIAL_OFFSET = 6000


class FixedWarpPoint(RoomLocation):
    def __init__(self, data: PortalData, offset: int):
        room = data.source_room.upper()
        super().__init__(f"Fixed Warp - {room}", "", [], offset, room)


def initialize() -> list[FixedWarpPoint]:
    return [FixedWarpPoint(data, INITIAL_OFFSET + i) for i, data in enumerate(portals)]


locations = initialize()


def select(options: RainWorldOptions) -> list[LocationData]:
    return locations if options.starting_scug == "Watcher" else []
