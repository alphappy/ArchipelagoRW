from .classes import EventData, VictoryEvent
from .. import RainWorldOptions
from ..conditions.classes import Simple, AllOf
from ..game_data.watcher import normal_regions
from ..locations.passages import generate_cond_pilgrim
from ..locations.foodquest import pips as fq_items

def generate(options: RainWorldOptions) -> list[EventData]:
    ascension = options.which_victory_condition == 0
    story = options.which_victory_condition == 1
    echoes = options.which_victory_condition == 2
    food_quest = options.which_victory_condition == 3
    weaver = options.which_victory_condition == 4
    true_ending = options.which_victory_condition == 5

    if options.starting_scug == "Watcher":
        if ascension:
            return [VictoryEvent("Spinning Top", "Ancient Urban")]
        if story:
            cond = AllOf(
                Simple("Ripple", 8),
                # For now, I'm just assuming that if you can access a region, you can rot it.
                # I can't think of any circumstance where this isn't the case,
                # even considering all the different dynamic warp options,
                # but I'm leaving this note here as a thing to investigate later just in case.
                Simple([f"Access-{r}" for r in normal_regions], options.rotted_region_target.value)
            )
            return [VictoryEvent("The Prince", "Outer Rim", cond)]
        if weaver:
            cond = AllOf(
                # With these conditions you should be able to get the Weaver ability
                # and close all the warps. This will have to change when Weaver
                # ability gets randomized
                Simple("Ripple", 8),
                Simple([f"Access-{r}" for r in [*normal_regions, "WARA"]])
            )
            return [VictoryEvent("An Understanding", "Events", cond)]
        if true_ending:
            pass


    # Watcher victory conditions should end with this one
    if options.which_victory_condition == 3:
        foods = [item.full_name for item in fq_items if item.should_generate(options)]
        # I sincerely apologize, the achievement based naming convention has been broken.
        return [VictoryEvent("Glutton", "Events", Simple(foods, locations=True))]

    # For Saint, the MS echo can be substituted in place of a normal echo.
    # For better or worse, this is not accounted for in logic.
    if options.which_victory_condition == 2:
        return [VictoryEvent("Pilgrimage", "Events", generate_cond_pilgrim(options))]

    # Saint's victory condition is different regardless of setting.
    if options.starting_scug == "Saint":
        return [VictoryEvent("Ascension", "Rubicon", Simple("Karma", 8))]

    # Sofanthiel has no alternate, and no alternate exists without MSC.
    if not story or not options.msc_enabled or options.starting_scug == "Inv":
        return [VictoryEvent("Ascension", "Subterranean Depths", Simple("Karma", 8))]

    if options.starting_scug in ["Yellow", "White"]:
        return [VictoryEvent("Journey's End", "Outer Expanse")]

    if options.starting_scug == "Red":
        return [VictoryEvent("A Helping Hand", "Shoreline", Simple("Slag Key"))]

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


