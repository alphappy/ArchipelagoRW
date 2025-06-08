from BaseClasses import MultiWorld
from .classes import LocationData, RoomLocation
from ..conditions.classes import Simple
from ..options import RainWorldOptions
from ..game_data.watcher import portals, PortalData, normal_regions, targets, WarpTargetData

INITIAL_OFFSET = 6000


class FixedWarpPoint(RoomLocation):
    def __init__(self, data: PortalData, offset: int):
        room = data.source_room.upper()
        super().__init__(f"Fixed Warp - {room}", f"Warp-{room}", [], offset, room)


class SpinningTop(RoomLocation):
    def __init__(self, data: PortalData, offset: int):
        room = data.source_room.upper()
        super().__init__("Spinning Top", f"SpinningTop-{room.split('_')[0]}", [], offset, room)


class Rottening(RoomLocation):
    def __init__(self, data: WarpTargetData, offset: int):
        room = data.room.upper()
        super().__init__("Spread the Rot", f"SpreadRot-{room.split('_')[0]}", [], offset, room)


class PrinceEncounter(RoomLocation):
    def __init__(self, offset: int, num: int):
        super().__init__(f"Prince encounter #{num}", f"Prince-{num}", [], offset, "WORA_AI")
        self.access_condition = Simple("Ripple", 2 * num)

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        self.progress_type = options.priority_throne.value
        return super().make(player, multiworld, options)


class ThroneWarp(RoomLocation):
    def __init__(self, offset: int, num: int):
        super().__init__(f"Create {self.names[num]} warp", f"ThroneWarp-{self.rooms[num]}", [], offset,
                         f"WORA_THRONE{self.rooms[num]}")
        self.access_condition = Simple("Ripple", 2 * num)

    rooms = [f"{a:0>2}" for a in (10, 5, 9, 7)]
    names = ["lower east", "lower west", "upper east", "upper west"]

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        self.progress_type = options.priority_throne.value
        return super().make(player, multiworld, options)


def initialize() -> tuple[list[FixedWarpPoint], list[SpinningTop], list[Rottening], list[PrinceEncounter], list[ThroneWarp]]:
    rottening = [[t for t in targets if t.room.startswith(r)][0] for r in normal_regions]

    return ([FixedWarpPoint(data, INITIAL_OFFSET + i) for i, data in enumerate(portals)],
            [SpinningTop(data, INITIAL_OFFSET + 100 + i) for i, data in enumerate(portals) if data.check_spinning_top],
            [Rottening(data, INITIAL_OFFSET + 130 + i) for i, data in enumerate(rottening)],
            [PrinceEncounter(INITIAL_OFFSET + 120 + i, i + 1) for i in range(4)],
            [ThroneWarp(INITIAL_OFFSET + 125 + i, i) for i in range(4)])


fixed_warps, spinning_tops, rottenings, encounters, thrones = initialize()


def select(options: RainWorldOptions) -> list[LocationData]:
    if options.starting_scug != "Watcher":
        return []
    ret = fixed_warps + spinning_tops + encounters + thrones
    if options.should_have_rot_spread_checks:
        ret += rottenings
    return ret
