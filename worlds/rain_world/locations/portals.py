from BaseClasses import MultiWorld
from .classes import LocationData, RoomLocation
from ..conditions import GameStateFlag
from ..game_data.general import scugs_all, scugs_vanilla
from ..options import RainWorldOptions
from ..game_data import static_data, general
from ..game_data.watcher import portals, PortalData

INITIAL_OFFSET = 6000


class FixedWarpPoint(RoomLocation):
    def __init__(self, data: PortalData, offset: int, spinning_top: bool = False):
        room = data.source_room.upper()
        super().__init__(f"{'Spinning Top' if spinning_top else 'Fixed Warp'} - {room}", "", [], offset, room)


def initialize() -> list[FixedWarpPoint]:
    return ([FixedWarpPoint(data, INITIAL_OFFSET + i) for i, data in enumerate(portals)] +
            [FixedWarpPoint(data, INITIAL_OFFSET + 100 + i, True) for i, data in enumerate(portals) if data.spinning_top])


locations = initialize()


def select(options: RainWorldOptions) -> list[LocationData]:
    return locations if options.starting_scug == "Watcher" else []
