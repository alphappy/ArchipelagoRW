from .classes import LocationData
from ..conditions.classes import Simple
from ..game_data.general import (food_quest_items, alt_food_quest_items, food_quest_saint_inedible,
                                 food_quest_spearmaster_inedible, food_quest_spearmaster_only,
                                 food_quest_large_creatures, food_quest_expanded_items, extreme_threat_creatures)
from ..options import RainWorldOptions

locations = {
    food:
    LocationData(
        f"FoodQuest-{food}", f"FoodQuest-{food}", "Food Quest", 5250 + i,
        Simple(alt_food_quest_items[food], 1) if food in alt_food_quest_items.keys() else Simple(food)
    ) for i, food in enumerate(food_quest_items + food_quest_expanded_items)
}


def generate(options: RainWorldOptions) -> list[LocationData]:
    if options.checks_foodquest.value == 0 or not options.msc_enabled:
        return []

    if (options.starting_scug == "Gourmand") + options.checks_foodquest.value > 1:
        foods = set(food_quest_items)
        if options.checks_foodquest_expanded:
            foods.update(food_quest_expanded_items)

        if options.starting_scug != "Spear":
            foods = foods.difference(food_quest_spearmaster_only)
        if options.starting_scug in {"White", "Yellow", "Rivulet", "Saint"}:
            foods = foods.difference(food_quest_large_creatures)
        if options.starting_scug == "Saint":
            foods = foods.difference(food_quest_saint_inedible)

        # HARDCODE: MLLs only exist for Rivulet.
        foods = foods.difference({"TerrorLongLegs"})

        if options.starting_scug == "Spear":
            foods = foods.difference(food_quest_spearmaster_inedible)
            # HARDCODE: Spearmaster doesn't find *actual* DLLs in their worldstate.
            foods = foods.difference({"DaddyLongLegs"})

        # HARDCODE: Hunter doesn't find Miros Vultures in their worldstate.
        elif options.starting_scug == "Red":
            foods = foods.difference({"MirosVulture"})
        # HARDCODE: Gourmand doesn't find Miros Vultures or elite scavs in their worldstate.
        elif options.starting_scug == "Gourmand":
            foods = foods.difference({"MirosVulture", "ScavengerElite"})
        # HARDCODE: Artificer doesn't find Glow Weed in their worldstate.
        elif options.starting_scug == "Artificer":
            foods = foods.difference({"GlowWeed"})
        # HARDCODE: Every vulture in Sofnathiel's worldstate is a Miros, and there are no elite scav dens.
        elif options.starting_scug == "Inv":
            foods = foods.difference({"Vulture", "KingVulture", "ScavengerElite"})
        # HARDCODE: Gourmand and Sofanthiel are the only ones who can both find and eat yeeks.
        if options.starting_scug not in ("Gourmand", "Inv"):
            foods = foods.difference({"Yeek"})
        # HARDCODE: Stawberry and train lizards don't exist in most worldstates.
        if options.starting_scug != "Inv":
            foods = foods.difference({"ZoopLizard", "TrainLizard"})

        if options.difficulty_extreme_threats + (options.starting_scug not in
                                                 ["Gourmand", "Artificer", "Spear", "Inv"]):
            foods = foods.difference(extreme_threat_creatures)

        return [locations[food] for food in foods]

    return []
