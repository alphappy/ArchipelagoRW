from .classes import LocationData, RoomLocation
from ..options import RainWorldOptions
from ..game_data.watcher import portals, PortalData

INITIAL_OFFSET = 6000


class FixedWarpPoint(RoomLocation):
    def __init__(self, data: PortalData, offset: int):
        room = data.source_room.upper()
        super().__init__(f"Fixed Warp - {room}", "", [], offset, room)


class SpinningTop(RoomLocation):
    def __init__(self, data: PortalData, offset: int):
        super().__init__("Spinning Top", "", [], offset, data.source_room.upper())


def initialize() -> list[RoomLocation]:
    return ([FixedWarpPoint(data, INITIAL_OFFSET + i) for i, data in enumerate(portals)] +
            [SpinningTop(data, INITIAL_OFFSET + 100 + i) for i, data in enumerate(portals) if data.check_spinning_top])


locations = initialize()


def select(options: RainWorldOptions) -> list[LocationData]:
    return locations if options.starting_scug == "Watcher" else []
