from random import Random

from BaseClasses import MultiWorld
from .classes import RegionData, ConnectionData, room_to_region
from ..options import RainWorldOptions
from ..conditions.classes import Simple, ConditionBlank, AllOf, AnyOf
from ..game_data.general import region_code_to_name


class DynamicWarpConnection(ConnectionData):
    def __init__(self, source: str, dest: str, ripple: float | None, sort: str,
                 source_room: bool = True, target_room: bool = True):
        self.ripple, self.source_room, self.target_room = ripple, source_room, target_room
        cond = Simple("Ripple", int((ripple - 1) * 2)) if ripple is not None else ConditionBlank
        super().__init__(source, dest, f"{sort} dynamic warp from {source} to {dest} ({ripple})", cond)

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        self.source = room_to_region[self.source] if self.source_room else self.source
        self.dest = room_to_region[self.dest] if self.target_room else self.dest
        super().make(player, multiworld, options)


class NormalDynamic(DynamicWarpConnection):
    def __init__(self, dest: str, ripple: float):
        super().__init__("From any normal region", dest, ripple, "Normal", False, True)


class PredeterminedNormalDynamic(DynamicWarpConnection):
    def __init__(self, source: str, dest: str, ripple: float, unlockable: bool = False):
        self.region_code = source
        self.unlockable = unlockable
        super().__init__(region_code_to_name[source], dest, ripple, "Predetermined normal", False, True)
        if unlockable:
            self.condition = AllOf(self.condition, Simple(f"Dynamic: {self.region_code}"))

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        multiworld.worlds[player].predetermined_warps[self.region_code] = self.dest
        super().make(player, multiworld, options)


class PredeterminedThroneDynamic(DynamicWarpConnection):
    def __init__(self, dest: str, ripple: float, which: int):
        super().__init__(self.rooms[which], dest, ripple, f"{self.names[which]} Throne", True, True)

    rooms = [f"WORA_THRONE{a:0>2}" for a in (10, 5, 9, 7)]
    names = ["Lower east", "Lower west", "Upper east", "Upper west"]

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        multiworld.worlds[player].predetermined_warps[self.source] = self.dest
        super().make(player, multiworld, options)


class PoolNormalDynamic(DynamicWarpConnection):
    def __init__(self, dest: str, ripple: float | None, unlockable: bool = False):
        self.unlockable = unlockable
        self.dest_region = dest.split("_")[0]
        super().__init__("From any normal region", dest, ripple, "Normal", False, True)
        if unlockable:
            self.condition = AllOf(self.condition, Simple(f"Dynamic: {self.dest_region}"))

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        multiworld.worlds[player].warp_pool.add(self.dest_region if self.unlockable else self.dest)
        super().make(player, multiworld, options)

cond_can_dynamic_warp = AnyOf(Simple("Ripple", 2), Simple("Dial Warp Ability"))

def generate(options: RainWorldOptions, rng: Random):
    if options.starting_scug != "Watcher":
        return []

    ret = [
        RegionData("From any normal region"),

        # Dial warp ability also grants the ability to dynamic warp
        ConnectionData("Menu", "From any normal region", "Create a dynamic warp",
                       cond_can_dynamic_warp),
        ConnectionData("From any normal region", "Crumbling Fringes", "Bad dynamic warp to Crumbling Fringes"),
        ConnectionData("From any normal region", "Corrupted Factories", "Bad dynamic warp to Corrupted Factories"),
        ConnectionData("From any normal region", "Decaying Tunnels", "Bad dynamic warp to Decaying Tunnels"),
        ConnectionData("From any normal region", "Infested Wastes", "Bad dynamic warp to Infested Wastes"),
    ]

    if options.logic_rotted_generation == 1:
        ret.append(ConnectionData("From any normal region", "Western Outer Rim", "Bad dynamic warp to Outer Rim",
                                  Simple("Ripple", 2)))

    return ret



