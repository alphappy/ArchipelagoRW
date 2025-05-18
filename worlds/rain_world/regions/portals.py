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
        # print(f"Defining connection from {self.source} to {self.dest}")  # DEBUG

        conds = []
        if self.data.should_have_key:
            conds.append(Simple(self.data.key_name))
        if self.data.ripple:
            conds.append(Simple("Ripple", 8))
        self.condition = AllOf(*conds)

        super().make(player, multiworld, options)


def generate(options: RainWorldOptions) -> list[PortalConnection]:
    if options.starting_scug != "Watcher":
        return []

    return [PortalConnection(data) for data in portals]

