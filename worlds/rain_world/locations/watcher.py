from BaseClasses import MultiWorld
from .classes import LocationData, RoomLocation
from ..conditions.classes import Simple, AllOf
from ..options import RainWorldOptions
from ..game_data.watcher import portals, PortalData, normal_regions, targets, WarpTargetData

INITIAL_OFFSET = 6000


class FixedWarpPoint(RoomLocation):
    def __init__(self, data: PortalData, offset: int):
        room = data.source_room.upper()
        super().__init__(f"Fixed Warp - {room}", f"Warp-{room}", ["Warp", "Fixed Warp"], offset, room)


class SpinningTop(RoomLocation):
    def __init__(self, data: PortalData, offset: int):
        room = data.source_room.upper()
        super().__init__("Spinning Top", f"SpinningTop-{room.split('_')[0]}", ["Spinning Top"], offset, room)


class Rottening(LocationData):
    def __init__(self, num: int, offset: int):
        cond = AllOf(Simple([f"Access-{r}" for r in normal_regions], num), Simple("Access-WORA"))
        super().__init__(f"Spread the Rot - Region #{num}", f"SpreadRot-{num}", ["Spread the Rot"], offset, "Menu", cond)


class PrinceEncounter(RoomLocation):
    def __init__(self, offset: int, num: int):
        super().__init__(f"Prince encounter #{num}", f"Prince-{num}", ["Prince", "The Prince", "Prince Encounter"], offset, "WORA_AI")
        self.access_condition = Simple("Ripple", 2 * num)

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        self.progress_type = options.priority_throne.value
        return super().make(player, multiworld, options)


class ThroneWarp(RoomLocation):
    def __init__(self, offset: int, num: int):
        super().__init__(f"Create {self.names[num]} warp", f"ThroneWarp-{self.rooms[num]}", ["Throne Warp"], offset,
                         f"WORA_THRONE{self.rooms[num]}")

    rooms = [f"{a:0>2}" for a in (10, 5, 7, 9)]
    names = ["lower east", "lower west", "upper east", "upper west"]

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        self.progress_type = options.priority_throne.value
        return super().make(player, multiworld, options)


def initialize() -> tuple[list[FixedWarpPoint], list[SpinningTop], list[Rottening], list[PrinceEncounter], list[ThroneWarp], list[LocationData]]:
    return ([FixedWarpPoint(data, INITIAL_OFFSET + i) for i, data in enumerate(portals)],
            [SpinningTop(data, INITIAL_OFFSET + 100 + i) for i, data in enumerate(portals) if data.check_spinning_top],
            [Rottening(i + 1, INITIAL_OFFSET + 150 + i) for i in range(len(normal_regions))],
            [PrinceEncounter(INITIAL_OFFSET + 120 + i, i + 1) for i in range(4)],
            [ThroneWarp(INITIAL_OFFSET + 125 + i, i) for i in range(4)],
            [RoomLocation("Meet Elder Ripple Spawn", "Meet_Ripple_Elder", [],
                          INITIAL_OFFSET + 130, "WORA_EGG")])


fixed_warps, spinning_tops, rottenings, encounters, thrones, unique = initialize()


def select(options: RainWorldOptions) -> list[LocationData]:
    if options.starting_scug != "Watcher":
        return []
    ret = fixed_warps + spinning_tops + encounters + thrones + unique
    if options.should_have_rot_spread_checks:
        ret += rottenings
    return ret
