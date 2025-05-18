from .classes import EventData, VictoryEvent
from .. import RainWorldOptions
from ..conditions.classes import Simple


def generate(options: RainWorldOptions) -> list[EventData]:
    alt = options.which_victory_condition == "alternate"

    if options.starting_scug == "Watcher":
        return [VictoryEvent("Peace", "Ancient Urban")]

    # Saint's victory condition is different regardless of setting.
    if options.starting_scug == "Saint":
        return [VictoryEvent("Ascension", "Rubicon", Simple("Karma", 8))]

    # Hunter and Sofanthiel have no alterante, and no alternate exists without MSC.
    if not alt or not options.msc_enabled or options.starting_scug in ["Red", "Inv"]:
        return [VictoryEvent("Ascension", "Subterranean Depths", Simple("Karma", 8))]

    if options.starting_scug in ["Yellow", "White"]:
        return [VictoryEvent("Journey's End", "Outer Expanse")]

    if options.starting_scug == "Rivulet":
        return [
            EventData("Install rarefaction cell", "Submerged Superstucture Heart", "Submerged Superstructure",
                      condition=Simple("Rarefaction Cell")),
            VictoryEvent("Old Friend", "Shoreline", Simple("Install rarefaction cell"))
        ]

    ret = [EventData("MeetFP", "MeetFP", "Five Pebbles above puppet")]

    if options.starting_scug == "Gourmand":
        ret.append(VictoryEvent("Migration", "Outer Expanse", Simple(["The Mark", "MeetFP"])))

    if options.starting_scug == "Artificer":
        ret.append(VictoryEvent("Closure", "Metropolis", Simple(["The Mark", "MeetFP"])))

    if options.starting_scug == "Spear":
        ret += [
            EventData("MeetLttM", "MeetLttM", "Looks to the Moon"),
            VictoryEvent("Messenger", "Sky Islands", Simple(
                ["The Mark", "MeetFP", "MeetLttM", "Moon's Final Message", "Spearmaster's Pearl"]
            ))
        ]

    return ret


