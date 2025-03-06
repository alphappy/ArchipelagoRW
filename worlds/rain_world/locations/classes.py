from typing import Optional, Callable

from BaseClasses import MultiWorld, Location
from ..options import RainWorldOptions
from ..conditions.classes import ConditionBlank, Condition
from ..constants import FIRST_ID
from worlds.generic.Rules import add_rule

location_map: dict[str, int] = {}


class LocationData:
    def __init__(self, full_name: str, short_name: str, region: str, offset: Optional[int],
                 access_condition: Condition = ConditionBlank,
                 generation_condition: Callable[[RainWorldOptions], bool] = lambda _: True,
                 access_condition_generator: Optional[Callable[[RainWorldOptions], Condition]] = None):
        self.full_name = full_name
        self.short_name = short_name
        self.region = region
        self.id = None
        self.access_condition = access_condition
        self.generation_condition = generation_condition
        self.access_condition_generator = access_condition_generator
        if offset is not None:
            self.id = offset + FIRST_ID
            location_map[full_name] = self.id

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        region = multiworld.get_region(self.region, player)
        if region.populate and self.generation_condition(options):
            loc = Location(player, self.short_name, self.id, region)
            region.locations.append(loc)
            if self.access_condition_generator is not None:
                add_rule(loc, self.access_condition_generator(options).check(player))
            elif self.access_condition is not ConditionBlank:
                add_rule(loc, self.access_condition.check(player))
            return self.id is not None
        return False


class PhysicalLocation(LocationData):
    def __init__(self, full_name: str, short_name: str, region: str, offset: int, room: str,
                 access_condition: Condition = ConditionBlank,
                 generation_condition: Callable[[RainWorldOptions], bool] = lambda _: True,
                 access_condition_generator: Optional[Callable[[RainWorldOptions], Condition]] = None):
        super().__init__(full_name, short_name, region, offset, access_condition, generation_condition,
                         access_condition_generator=access_condition_generator)
        self.room = room


class Passage(LocationData):
    def __init__(self, name: str, region: str, offset: int,
                 access_condition: Condition = ConditionBlank,
                 access_condition_generator:  Optional[Callable[[RainWorldOptions], Condition]] = None):
        super().__init__(f"Passage-{name}", f"Passage-{name}", region, offset, access_condition,
                         access_condition_generator=access_condition_generator)
