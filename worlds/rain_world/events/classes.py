from BaseClasses import ItemClassification, MultiWorld, Item, Location, CollectionState
from worlds.generic.Rules import add_rule
from ..options import RainWorldOptions
from ..game_data.general import scugs_all
from ..conditions.classes import Condition, ConditionBlank


class EventData:
    def __init__(self, item_name: str, location_name: str, region: str,
                 classification: ItemClassification = ItemClassification.progression,
                 condition: Condition = None):
        self.item_name = item_name
        self.location_item = location_name
        self.region = region
        self.classification = classification
        self.condition = condition

    def make(self, player: int, multiworld: MultiWorld, _: RainWorldOptions):
        region = multiworld.get_region(self.region, player)
        if region.populate:
            item = Item(self.item_name, self.classification, None, player)
            location = Location(player, self.location_item, None, region)
            location.show_in_spoiler = False
            region.locations.append(location)
            location.place_locked_item(item)
            if self.condition is not None:
                add_rule(location, self.condition.check(player))


class VictoryEvent(EventData):
    def __init__(self, location_name: str, region: str, condition: Condition = None):
        # Note: events have to be progression even if they're not used in the condition for another conn/loc
        super().__init__("Victory", location_name, region, condition=condition)


class StaticWorldEvent:
    def __init__(self, item_name: str, location_name: str, region: str, condition: Condition = ConditionBlank,
                 scugs: set[str] = scugs_all):
        self.item_name = item_name
        self.location_item = location_name
        self.region = region
        self.classification = ItemClassification.progression
        self.condition = condition
        self.scugs = scugs

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        if options.starting_scug not in self.scugs:
            return
        try:
            region = multiworld.get_region(self.region, player)
        except KeyError:
            return

        if region.populate:
            item = Item(self.item_name, self.classification, None, player)
            location = Location(player, self.location_item, None, region)
            location.show_in_spoiler = False
            region.locations.append(location)
            location.place_locked_item(item)
            add_rule(location, self.condition.check(player))