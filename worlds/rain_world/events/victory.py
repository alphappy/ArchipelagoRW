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
    true_ending = options.which_victory_condition == 4

    if options.starting_scug == "Watcher":
        if ascension: # Spinning Top
            return [VictoryEvent("Spinning Top", "Ancient Urban")]
        if story: # Rot
            cond = AllOf(
                Simple("Ripple", 3 + options.logic_ripplespace_min_req),
                Simple([f"Access-{r}" for r in normal_regions], options.rotted_region_target.value)
            )
            return [VictoryEvent("The Prince", "Outer Rim", cond)]
        if echoes: # Weaver
            cond = Simple([f"Access-{r}" for r in [*normal_regions, "WARA"]])
            if options.weaver_randomized:
                cond = AllOf(cond, Simple("Progressive Weaver", 4))
            else:
                # Ripple 9 not technically required, but is needed to find Weaver spots "naturally" rather than looking at a map
                cond = AllOf(cond, Simple("Ripple", 3 + options.logic_ripplespace_min_req))

            return [VictoryEvent("An Understanding", "Events", cond)]
        if true_ending: # True Ending
            # Must be able to reach Ancient Urban for Spinning Top ending,
            # Outer Rim and enough Ripple to wake the Prince,
            # Weaver ability if it was randomized,
            # And every normal region for warp sealing.
            # Ripple requirement handled by Daemon access
            cond = Simple([f"Access-{r}" for r in [*normal_regions, "WARA", "WAUA", "WORA"]])
            if options.weaver_randomized:
                cond = AllOf(cond, Simple("Progressive Weaver", 4))

            return [VictoryEvent("The Choice", "Daemon", cond)]


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

    if options.starting_scug == "Gourmand":
        return [VictoryEvent("Migration", "Outer Expanse")]

    if options.starting_scug == "Artificer":
        return [VictoryEvent("Closure", "Metropolis")]

    if options.starting_scug == "Spear":
        return [VictoryEvent("Messenger", "Sky Islands", Simple(["Moon's Final Message", "Spearmaster's Pearl"]))]

    return []


