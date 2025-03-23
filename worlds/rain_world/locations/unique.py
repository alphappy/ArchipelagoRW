from .classes import LocationData, AbstractLocation, RoomLocation
from ..options import RainWorldOptions
from ..conditions.classes import Simple, Condition, ConditionBlank


class RoomLocationSimpleAccess(RoomLocation):
    def __init__(self, description: str, alt_names: list[str] | None, offset: int | None, room: str,
                 access_condition: Condition = ConditionBlank):
        super().__init__(description, alt_names[0], alt_names[1:], offset, room)
        self.access_condition = access_condition


locations = {
    "Eat_Neuron": AbstractLocation("Eat a Neuron Fly", "Eat_Neuron", [], 4900, "Events", Simple("SSOracleSwarmer")),
    "Gift_Neuron": RoomLocationSimpleAccess(
        "Give a Neuron Fly to Looks to the Moon", ["Gift_Neuron"], 4901, "SL_AI", Simple(["Access-SL", "Access-SS"])),
    "Meet_FP": RoomLocationSimpleAccess("Meet Five Pebbles", ["Meet_FP"], 4902, "SS_AI", Simple("The Mark")),
    "Meet_LttM": RoomLocationSimpleAccess("Meet Looks to the Moon", ["Meet_LttM"], 4903, "SL_AI", Simple("The Mark")),
    "Meet_LttM_Spear": RoomLocationSimpleAccess("Meet Looks to the Moon", ["Meet_LttM_Spear"], 4904, "DM_AI"),
    "Kill_FP": RoomLocationSimpleAccess("Remove Rarefaction Cell", ["Kill_FP"], 4905, "RM_CORE"),
    "Save_LttM": RoomLocationSimpleAccess(
        "Revive Looks to the Moon", ["Save_LttM"], 4906, "SL_AI", Simple("Slag Key")),
    "Ascend_FP": RoomLocationSimpleAccess("Ascend Five Pebbles", ["Ascend_FP"], 4907, "CL_AI", Simple("Karma", 8)),
    "Ascend_LttM": RoomLocationSimpleAccess(
        "Ascend Looks to the Moon", ["Ascend_LttM"], 4908, "SL_AI", Simple("Karma", 8)),
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
