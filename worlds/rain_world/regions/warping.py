from .classes import RainWorldRegion, RegionData, ConnectionData
from ..options import RainWorldOptions
from ..conditions.classes import Simple


def generate(options: RainWorldOptions):
    if options.starting_scug != "Watcher":
        return []

    return [
        RegionData("Dynamic warp"),

        ConnectionData("Menu", "Dynamic warp", "Create a dynamic warp", Simple("Ripple", 2)),
        ConnectionData("Dynamic warp", "Crumbling Fringes", "Bad dynamic warp to Crumbling Fringes"),
        ConnectionData("Dynamic warp", "Corrupted Factories", "Bad dynamic warp to Corrupted Factories"),
        ConnectionData("Dynamic warp", "Decaying Tunnels", "Bad dynamic warp to Decaying Tunnels"),
        ConnectionData("Dynamic warp", "Infested Wastes", "Bad dynamic warp to Infested Wastes"),
    ]



