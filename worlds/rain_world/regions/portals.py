from BaseClasses import MultiWorld
from .classes import ConnectionData
from ..conditions.classes import AllOf, Simple
from ..game_data.watcher import portals, PortalData
from ..game_data.general import region_code_to_name
from ..options import RainWorldOptions
from ..regions.classes import room_to_region


class PortalConnection(ConnectionData):
    def __init__(self, data: PortalData):
        self.data = data
        s = "Spinning Top" if data.spinning_top else "Fixed warp"
        super().__init__(data.source_room, data.target_room, f"{s} in {data.source_room}")

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        self.source, self.dest = room_to_region[self.data.source_room], room_to_region[self.data.target_room]

        conds = []

        if self.data.source_room[:4] in ["WHIR", "WDSR", "WGWR", "WSUR"]:
            if options.logic_rotted_generation != 2:
                return
            # Warps to WORA need specifically Ripple 3 (In case dynamic warp ability was acquired another way)
            conds.append(Simple("Ripple", 2))

        if (self.data.should_have_key
                and (not self.data.spinning_top or options.spinning_top_keys)
                and ("Daemon" not in self.data.key_name or options.daemon_keys)):
            conds.append(Simple(self.data.key_name))
        if self.data.ripple:
            conds.append(Simple("Ripple", 3 + options.logic_ripplespace_min_req))
        self.condition = AllOf(*conds)

        super().make(player, multiworld, options)


def generate(options: RainWorldOptions) -> list[PortalConnection]:
    if options.starting_scug != "Watcher":
        return []

    return [PortalConnection(data) for data in portals]

