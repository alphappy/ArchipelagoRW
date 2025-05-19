from random import Random

from BaseClasses import MultiWorld
from .classes import RainWorldRegion, RegionData, ConnectionData, room_to_region
from ..options import RainWorldOptions
from ..conditions.classes import Simple
from ..game_data.watcher import targets, normal_regions
from ..game_data.general import region_code_to_name
from ..utils import random_bijective_endofunction


class NormalDynamic(ConnectionData):
    def __init__(self, dest: str, ripple: float):
        self.ripple = ripple
        cond = Simple("Ripple", int((ripple - 1) * 2))
        super().__init__("From any normal region", dest, f"Normal dynamic warp to {dest} ({ripple})", cond)

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        self.dest = room_to_region[self.dest]
        super().make(player, multiworld, options)


class PredeterminedNormalDynamic(ConnectionData):
    def __init__(self, source: str, dest: str, ripple: float):
        cond = Simple("Ripple", int((ripple - 1) * 2))
        self.region_code = source
        super().__init__(region_code_to_name[source], dest, f"Normal dynamic warp to {dest} ({ripple})", cond)

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        multiworld.worlds[player].predetermined_warps[self.region_code] = self.dest
        self.dest = room_to_region[self.dest]
        super().make(player, multiworld, options)


def generate(options: RainWorldOptions, rng: Random):
    if options.starting_scug != "Watcher":
        return []

    ret = [
        RegionData("From any normal region"),

        ConnectionData("Menu", "From any normal region", "Create a dynamic warp", Simple("Ripple", 2)),
        ConnectionData("From any normal region", "Crumbling Fringes", "Bad dynamic warp to Crumbling Fringes"),
        ConnectionData("From any normal region", "Corrupted Factories", "Bad dynamic warp to Corrupted Factories"),
        ConnectionData("From any normal region", "Decaying Tunnels", "Bad dynamic warp to Decaying Tunnels"),
        ConnectionData("From any normal region", "Infested Wastes", "Bad dynamic warp to Infested Wastes"),
    ]

    match options.normal_dynamic_warp_behavior:
        case 3:  # open world
            for target in targets:
                ret.append(NormalDynamic(target.room, target.ripple))

        case 5:  # predetermined
            for source, target_region in random_bijective_endofunction(normal_regions, rng).items():
                target = rng.sample([t for t in targets if t.room.startswith(target_region)], 1)[0]
                ret.append(PredeterminedNormalDynamic(source, target.room, target.ripple))

    return ret



