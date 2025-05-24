from .classes import LocationData, RoomLocation
from ..options import RainWorldOptions
from ..game_data.watcher import portals, PortalData, normal_regions, targets, WarpTargetData

INITIAL_OFFSET = 6000


class FixedWarpPoint(RoomLocation):
    def __init__(self, data: PortalData, offset: int):
        room = data.source_room.upper()
        super().__init__(f"Fixed Warp - {room}", "", [], offset, room)


class SpinningTop(RoomLocation):
    def __init__(self, data: PortalData, offset: int):
        super().__init__("Spinning Top", "", [], offset, data.source_room.upper())


class Rottening(RoomLocation):
    def __init__(self, data: WarpTargetData, offset: int):
        super().__init__("Spread the Rot", "", [], offset, data.room.upper())


def initialize() -> tuple[list[FixedWarpPoint], list[SpinningTop], list[Rottening]]:
    rottening = [[t for t in targets if t.room.startswith(r)][0] for r in normal_regions]

    return ([FixedWarpPoint(data, INITIAL_OFFSET + i) for i, data in enumerate(portals)],
            [SpinningTop(data, INITIAL_OFFSET + 100 + i) for i, data in enumerate(portals) if data.check_spinning_top],
            [Rottening(data, INITIAL_OFFSET + 130 + i) for i, data in enumerate(rottening)])


fixed_warps, spinning_tops, rottenings = initialize()


def select(options: RainWorldOptions) -> list[LocationData]:
    if options.starting_scug != "Watcher":
        return []
    ret = fixed_warps + spinning_tops
    if options.should_have_rot_spread_checks:
        ret += rottenings
    return ret
