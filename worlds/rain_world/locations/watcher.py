from BaseClasses import MultiWorld
from .classes import LocationData, RoomLocation
from ..conditions.classes import Simple, AllOf
from ..options import RainWorldOptions
from ..game_data.watcher import portals, PortalData, normal_regions
from ..regions.warping import cond_can_dynamic_warp

INITIAL_OFFSET = 6000


class FixedWarpPoint(RoomLocation):
    def __init__(self, data: PortalData, offset: int):
        room = data.source_room.upper()
        super().__init__(f"Fixed Warp - {room}", f"Warp-{room}", ["Warp", "Fixed Warp"], offset, room)

    def pre_generate(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        if self.room == "WARA_P09":
            self.access_condition = Simple("Ripple", 3 + options.logic_ripplespace_min_req)
        return super().pre_generate(player, multiworld, options)


class SpinningTop(RoomLocation):
    def __init__(self, data: PortalData, offset: int):
        room = data.source_room.upper()
        super().__init__("Spinning Top", f"SpinningTop-{room.split('_')[0]}", ["Spinning Top"], offset, room)

    def pre_generate(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        if self.room == "WARA_P09":
            self.access_condition = Simple("Ripple", 3 + options.logic_ripplespace_min_req)
        return super().pre_generate(player, multiworld, options)


class Rottening(LocationData):
    def __init__(self, num: int, offset: int):
        cond = AllOf(Simple([f"Access-{r}" for r in normal_regions], num), Simple("Access-WORA"))
        super().__init__(f"Spread the Rot - Region #{num}", f"SpreadRot-{num}", ["Spread the Rot"], offset, "Menu", cond)


class WeaverEncounter(LocationData):
    def __init__(self, num: int, offset: int):
        cond = AllOf(Simple([f"Access-{r}" for r in normal_regions], 2), cond_can_dynamic_warp)
        super().__init__(f"Weaver Encounter #{num}", f"Weaver-{num}", ["Weaver", "Weaver Encounter"], offset, "Menu", cond)


class PrinceEncounter(RoomLocation):
    def __init__(self, offset: int, num: int):
        super().__init__(f"Prince Encounter #{num}", f"Prince-{num}", ["Prince", "The Prince", "Prince Encounter"], offset, "WORA_AI")
        self.access_condition = Simple("Ripple", 2 * num)

    def pre_generate(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        self.progress_type = options.priority_throne.value
        return super().pre_generate(player, multiworld, options)


def initialize() -> tuple[list[FixedWarpPoint], list[SpinningTop], list[Rottening], list[WeaverEncounter], list[PrinceEncounter], list[LocationData]]:
    return ([FixedWarpPoint(data, INITIAL_OFFSET + i) for i, data in enumerate(portals) if data.check_warp],
            [SpinningTop(data, INITIAL_OFFSET + 100 + i) for i, data in enumerate(portals) if data.check_spinning_top],
            [Rottening(i + 1, INITIAL_OFFSET + 150 + i) for i in range(len(normal_regions))],
            [WeaverEncounter(i + 1, INITIAL_OFFSET + 140 + i) for i in range(4)],
            [PrinceEncounter(INITIAL_OFFSET + 120 + i, i + 1) for i in range(4)],
            [RoomLocation("Meet Elder Ripple Spawn", "Meet_Ripple_Elder", [],
                          INITIAL_OFFSET + 130, "WORA_EGG")])


fixed_warps, spinning_tops, rottenings, weaver_encounters, prince_encounters, unique = initialize()


def select(options: RainWorldOptions) -> list[LocationData]:
    if options.starting_scug != "Watcher":
        return []
    ret = fixed_warps + spinning_tops + prince_encounters + unique
    if options.should_have_rot_spread_checks:
        ret += rottenings
    if options.should_have_weaver_checks:
        ret += weaver_encounters
    return ret
