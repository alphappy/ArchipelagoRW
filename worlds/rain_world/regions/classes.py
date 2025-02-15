from typing import Callable

from BaseClasses import Region, MultiWorld
from ..game_data.general import scugs_all
from ..options import RainWorldOptions
from ..conditions.classes import Simple, Compound, Condition, ConditionBlank


class RainWorldRegion(Region):
    game = "Rain World"

    def __init__(self, name: str, player: int, multiworld: MultiWorld, populate: bool = True):
        super().__init__(name, player, multiworld)
        self.populate = populate


class Room(RainWorldRegion):
    pass


class RegionData:
    def __init__(self, name: str, generation_condition: Callable[[RainWorldOptions], bool] = lambda _: True):
        self.name = name
        self.generation_condition = generation_condition

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        multiworld.regions.append(RainWorldRegion(self.name, player, multiworld, self.generation_condition(options)))


class RoomData(RegionData):
    def __init__(self, name: str, scugs: list[str]):
        super().__init__(name)
        self.scugs = scugs

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        multiworld.regions.append(Room(self.name, player, multiworld, self.generation_condition(options)))


class ConnectionData:
    def __init__(self, source: str, dest: str, access_condition: Condition = ConditionBlank):
        self.source = source
        self.dest = dest
        self.access_condition = access_condition

    def make(self, player: int, multiworld: MultiWorld):
        source = multiworld.get_region(self.source, player)
        dest = multiworld.get_region(self.dest, player)
        # conditions = [
        #     Simple("Karma", self.cost - (1 if self.cost < 6 else 2)),
        #     Simple(f"GATE_{self.gate_name}"),
        #     self.condition
        # ]
        # rule = Compound(len(conditions), *conditions)
        if source.populate and dest.populate:
            source.connect(dest)


class RoomConnection(ConnectionData):
    def __init__(self, source: str, dest: str, scugs: set[str]):
        super().__init__(source, dest)
        self.scugs = set(scugs)  # explicit conversion to set necessary for unknown reason

    def make(self, player: int, multiworld: MultiWorld):
        source = multiworld.get_region(self.source, player)
        dest = multiworld.get_region(self.dest, player)

        if source.populate and dest.populate:
            source.connect(dest, rule=Simple([f"Scug-{s}" for s in self.scugs], 1).check(player))


