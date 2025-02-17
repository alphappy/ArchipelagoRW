from .classes import EventData, VictoryEvent
from .. import RainWorldOptions
from ..conditions.classes import Simple


def generate(options: RainWorldOptions) -> list[EventData]:
    alt = options.which_victory_condition == "alternate"

    # Saint's victory condition is different regardless of setting.
    if options.starting_scug == "Saint":
        return [VictoryEvent("Ascension", "HR_FINAL", Simple("Karma", 8))]

    # Hunter and Sofanthiel have no alterante, and no alternate exists without MSC.
    if not alt or not options.msc_enabled or options.starting_scug in ["Red", "Inv"]:
        return [VictoryEvent("Ascension", "SB_L01", Simple("Karma", 8))]

    if options.starting_scug in ["Yellow", "White"]:
        return [VictoryEvent("Journey's End", "OE_FINAL03")]

    if options.starting_scug == "Rivulet":
        return [
            VictoryEvent("Old Friend", "SL_AI", Simple(["The Mark", "Object-EnergyCell"]))
        ]

    ret = [EventData("MeetFP", "MeetFP", "SS_AI")]

    if options.starting_scug == "Gourmand":
        ret.append(VictoryEvent("Migration", "OE_FINAL03", Simple(["The Mark", "MeetFP"])))

    if options.starting_scug == "Artificer":
        ret.append(VictoryEvent("Closure", "LC_FINAL", Simple(["The Mark", "MeetFP"])))

    if options.starting_scug == "Spear":
        ret += [
            EventData("MeetLttM", "MeetLttM", "DM_AI"),
            VictoryEvent("Messenger", "SI_A07", Simple(
                ["The Mark", "MeetFP", "MeetLttM", "Rewrite_Spear_Pearl", "PearlObject-Spearmasterpearl"]
            ))
        ]

    return ret


