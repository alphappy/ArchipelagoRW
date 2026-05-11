from typing import Optional, Callable

from BaseClasses import MultiWorld, Location, LocationProgressType
from ..game_data.bitflag import ScugFlagMap
from ..game_data.watcher import watcher_high_up_shinies
from ..options import RainWorldOptions
from ..conditions.classes import ConditionBlank, Condition, AnyOf, Simple
from ..constants import FIRST_ID
from ..regions.classes import room_to_region
from ..game_data.general import region_code_to_name
from ..utils_ap import try_get_region
from ...AutoWorld import World

location_map: dict[str, int] = {}
location_hints: dict[str, set[str]] = {}
location_client_map: dict[str, str] = {}


class LocationData:
    def __init__(self, full_name: str, client_name: str, alt_names: list[str] | None, offset: int,
                 region: str = "Menu", access_condition: Condition = ConditionBlank):
        """Represents a location of any type."""
        self.full_name = full_name
        self.client_name = client_name
        self.alt_names = alt_names or []
        self.loc = None
        self.region = region
        self.access_condition: Condition = access_condition
        self.progress_type: LocationProgressType = LocationProgressType.DEFAULT
        self.whitelist: ScugFlagMap | None = None

        self.id = offset + FIRST_ID
        location_map[full_name] = self.id
        for alt_name in self.alt_names + [client_name]:
            if alt_name != full_name:
                location_hints.setdefault(alt_name, set()).update({full_name})
        location_client_map[client_name] = self.full_name

    def make(self, world: World, options: RainWorldOptions):
        """Resolve the rules on the location"""
        # self.loc is not None and
        if self.access_condition is not ConditionBlank:
            world.set_rule(self.loc, self.access_condition.get_rule())
            # add_rule(loc, self.access_condition.check(player))

    def pre_generate(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        """Create the location, or return False if the location should not be generated."""
        if self.whitelist is not None and not options.satisfies_flagmap(self.whitelist):
            return False

        if (region := try_get_region(multiworld, self.region, player)) and region.populate:
            self.loc = Location(player, self.full_name, self.id, region)
            self.loc.progress_type = self.progress_type
            region.locations.append(self.loc)
            return True

        return False

    def use_whitelist(self): self.whitelist = ScugFlagMap()


class RoomLocation(LocationData):
    def __init__(self, description: str, client_name: str, alt_names: list[str] | None, offset: int,
                 room: str):
        """
        Represents a location that exists in a specific room.
        """
        full_with_code = f'{room.split("_")[0]} - {description}'
        region_name = region_code_to_name[room.split("_")[0]]
        super().__init__(f'{region_name} - {description}',
                         client_name, alt_names + [region_name, full_with_code], offset)
        self.room = room


    def pre_generate(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        self.region = room_to_region[self.room]

        if not options.submerged_should_populate:
            if self.region in ("Submerged Superstructure", "Bitter Aerie", "Shoreline above puppet room",
                               "Shoreline near gate to Submerged"):
                return False
        if options.starting_scug == "Watcher" and self.client_name in watcher_high_up_shinies:
            self.access_condition = AnyOf(Simple("Ripple", 4), Simple("Explosive Jump Perk"))

        return super().pre_generate(player, multiworld, options)


class AbstractLocation(LocationData):
    def __init__(self, name: str, client_name: str, alt_names: list[str], offset: int, region: str,
                 access_condition: Condition = ConditionBlank,
                 access_condition_generator:  Optional[Callable[[RainWorldOptions], Condition]] = None):
        super().__init__(name, client_name, alt_names, offset, region, access_condition)
        self.acc_gen = access_condition_generator

    def pre_generate(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        if self.acc_gen is not None:
            self.access_condition = self.acc_gen(options)
        return super().pre_generate(player, multiworld, options)


class Passage(AbstractLocation):
    def __init__(self, name: str, region: str, offset: int,
                 access_condition: Condition = ConditionBlank,
                 access_condition_generator:  Optional[Callable[[RainWorldOptions], Condition]] = None):
        super().__init__(f"Passage - {self.proper_name(name)}", f"Passage-{name}", ["Passage"],
                         offset, region, access_condition, access_condition_generator)

    @staticmethod
    def proper_name(name: str):
        if name == "Traveller":
            return "The Wanderer"
        elif name == "DragonSlayer":
            return "The Dragon Slayer"
        return f'The {name}'