from BaseClasses import MultiWorld
from .classes import RainWorldRegion, RegionData, ConnectionData, room_to_region
from ..options import RainWorldOptions
from ..conditions.classes import Simple
from ..game_data.watcher import targets


class NormalDynamic(ConnectionData):
    def __init__(self, dest: str, ripple: float):
        self.ripple = ripple
        cond = Simple("Ripple", int((ripple - 1) * 2))
        super().__init__("Dynamic warp", dest, f"Normal dynamic warp to {dest} ({ripple})", cond)

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        self.dest = room_to_region[self.dest]
        super().make(player, multiworld, options)


def generate(options: RainWorldOptions):
    if options.starting_scug != "Watcher":
        return []

    ret = [
        RegionData("Dynamic warp"),

        ConnectionData("Menu", "Dynamic warp", "Create a dynamic warp", Simple("Ripple", 2)),
        ConnectionData("Dynamic warp", "Crumbling Fringes", "Bad dynamic warp to Crumbling Fringes"),
        ConnectionData("Dynamic warp", "Corrupted Factories", "Bad dynamic warp to Corrupted Factories"),
        ConnectionData("Dynamic warp", "Decaying Tunnels", "Bad dynamic warp to Decaying Tunnels"),
        ConnectionData("Dynamic warp", "Infested Wastes", "Bad dynamic warp to Infested Wastes"),
    ]

    if options.normal_dynamic_warp_behavior.logically_relevant:
        for target in targets:
            ret.append(NormalDynamic(target.room, target.ripple))

    return ret



