from .classes import LocationData
from ..conditions.classes import Simple
from ..game_data.general import (food_quest_items, alt_food_quest_items, food_quest_saint_inedible,
                                 food_quest_spearmaster_inedible, food_quest_survivor_inedible)
from ..options import RainWorldOptions

locations = {
    food:
    LocationData(
        f"FoodQuest-{food}", f"FoodQuest-{food}", "Food Quest", 5250 + i,
        Simple(alt_food_quest_items[food], 1) if food in alt_food_quest_items.keys() else Simple(food)
    ) for i, food in enumerate(food_quest_items)
}


def generate(options: RainWorldOptions) -> list[LocationData]:
    if options.checks_foodquest.value == 0 or not options.msc_enabled:
        return []

    foods = set(food_quest_items)

    if options.starting_scug != "Gourmand":
        if options.checks_foodquest.value == 2:
            if options.starting_scug in ["White", "Yellow", "Rivulet"]:
                foods = foods.difference(food_quest_survivor_inedible)
            elif options.starting_scug == "Spear":
                foods = foods.difference(food_quest_spearmaster_inedible)
            elif options.starting_scug == "Saint":
                foods = foods.difference(food_quest_saint_inedible)
            # HARDCODE: Artificer doesn't find Glow Weed in their world state.
            elif options.starting_scug == "Artificer":
                foods = foods.difference({"GlowWeed"})

            # Hunter and Sofanthiel can complete the food quest.

        else:  # not gourmand and food quest set to gourmand-only
            return []

    return [locations[food] for food in foods]
