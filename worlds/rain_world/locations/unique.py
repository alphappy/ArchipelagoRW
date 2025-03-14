from .classes import LocationData, AbstractLocation
from ..options import RainWorldOptions
from ..conditions.classes import Simple

locations = {
    "Eat_Neuron": AbstractLocation("Eat_Neuron", [], 4900, "Events", Simple("SSOracleSwarmer")),
    "Gift_Neuron": AbstractLocation("Gift_Neuron", [], 4901, "Events", Simple(["Access-SL", "Access-SS"])),
    "Meet_FP": AbstractLocation("Meet_FP", [], 4902, "Five Pebbles above puppet", Simple("The Mark")),
    "Meet_LttM": AbstractLocation("Meet_LttM", [], 4903, "Shoreline", Simple("The Mark")),
    "Meet_LttM_Spear": AbstractLocation("Meet_LttM_Spear", [], 4904, "Looks to the Moon"),
    "Kill_FP": AbstractLocation("Kill_FP", [], 4905, "The Rot"),
    "Save_LttM": AbstractLocation("Save_LttM", [], 4906, "Shoreline", Simple("Object-NSHSwarmer")),
    "Ascend_FP": AbstractLocation("Ascend_FP", [], 4907, "Silent Construct", Simple("Karma", 8)),
    "Ascend_LttM": AbstractLocation("Ascend_LttM", [], 4908, "Shoreline", Simple("Karma", 8)),
}


def generate(options: RainWorldOptions) -> list[LocationData]:
    keys = ["Eat_Neuron"]

    if options.starting_scug in ["Yellow", "White", "Gourmand"]:
        keys.append("Gift_Neuron")

    if options.starting_scug in ["Yellow", "White", "Red", "Gourmand", "Artificer", "Spear", "Inv"]:
        keys.append("Meet_FP")

    if options.starting_scug in ["Yellow", "White", "Red", "Gourmand", "Rivulet", "Saint"]:
        keys.append("Meet_LttM")

    if options.starting_scug == "Red":
        keys.append("Save_LttM")

    if options.starting_scug == "Spear":
        keys.append("Meet_LttM_Spear")

    if options.starting_scug == "Rivulet":
        keys.append("Kill_FP")

    if options.starting_scug == "Saint":
        keys += ["Ascend_FP", "Ascend_LttM"]

    return [locations[key] for key in keys]
