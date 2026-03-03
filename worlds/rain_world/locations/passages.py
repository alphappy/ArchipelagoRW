from .classes import Passage, LocationData
from .. import game_data
from ..game_data.general import regions_all, watcher_pearls
from ..options import RainWorldOptions
from ..conditions.classes import Condition, Simple, AnyOf, AllOf, ConditionBlank


#################################################################
# SURVIVOR
def generate_cond_survivor(options: RainWorldOptions) -> Condition:
    if options.starting_scug == "Watcher":
        return ConditionBlank
    return Simple("Karma", 4)


#################################################################
# CHIEFTAIN
def generate_cond_chieftain(options: RainWorldOptions) -> Condition:
    return Simple("Toll") if options.difficulty_chieftain else Simple(["Scavenger", "ScavengerElite"], 1)


#################################################################
# DRAGON SLAYER
def generate_cond_dragonslayer(options: RainWorldOptions) -> Condition:
    if not options.msc_enabled:
        return Simple(game_data.general.dragonslayer_vanilla)
    if options.difficulty_extreme_threats:
        return Simple(game_data.general.dragonslayer_msc, 6)
    else:
        return Simple(game_data.general.dragonslayer_msc.difference({"RedLizard"}), 6)


#################################################################
# FRIEND
cond_friend = Simple(game_data.general.lizards_any, 1)


#################################################################
# HUNTER
def generate_cond_hunter(options: RainWorldOptions) -> Condition:
    # Carnivorous slugcats use simple region check
    if options.starting_scug in ["Red", "Artificer", "Spear", "Gourmand", "Inv"]:
        return Simple([f"Access-{region}" for region in set(game_data.general.regions_all).difference({"SS", "MS"})], 1)
    return Simple(
            ["Fly", "SmallNeedleWorm", "SmallCentipede", "Centipede",
             "EggBug", "JellyFish", "Hazer", "VultureGrub", "Frog", "Tardigrade",
             "SandGrubNetwork", "PlacedRats", "Barnacle"],
            options.difficulty_hunter.value
        )


#################################################################
# MONK
def generate_cond_monk(options: RainWorldOptions) -> Condition:
    if options.starting_scug in ["Spear", "Artificer", "Red"]:
        return Simple(["Access-SI", "Access-LF", "Access-SS", "Access-DM"], 1)
    foods = [
        *game_data.general.monk_foods_vanilla,
        *(game_data.general.monk_foods_msc if options.msc_enabled else []),
        *(game_data.general.monk_foods_watcher if options.is_watcher_enabled else []),
     ]
    return Simple(foods, options.difficulty_monk.value)


#################################################################
# MOTHER
cond_mother = Simple([f"Access-{region}" for region in game_data.general.slugpup_normal_regions], 1)


#################################################################
# NOMAD
def generate_cond_nomad(options: RainWorldOptions) -> Condition:
    return Simple([f"Access-{region}" for region in game_data.general.regions_all], options.difficulty_nomad.value)


#################################################################
# OUTLAW
def generate_cond_outlaw(options: RainWorldOptions) -> Condition:
    return Simple(
        list(game_data.general.outlaw_whitelist if options.difficulty_extreme_threats else
             game_data.general.outlaw_whitelist.difference(game_data.general.extreme_threat_creatures)),
        options.difficulty_outlaw.value
    )


#################################################################
# PILGRIM
def generate_cond_pilgrim(options: RainWorldOptions) -> Condition:
    if options.starting_scug == "Saint":
        echoes = ["CC", "SI", "LF", "SB", "UG", "SL", "CL"]
    elif options.starting_scug == "Artificer":
        echoes = ["CC", "SI", "LF", "SB", "UW", "SH", "LC"]
    else:
        echoes = ["CC", "SI", "LF", "SB", "UW", "SH"]

    return Simple([f"{game_data.general.region_code_to_name[e]} - Echo" for e in echoes], locations=True)


#################################################################
# SCHOLAR
def generate_cond_scholar(options: RainWorldOptions) -> Condition:
    if options.starting_scug in ["Yellow", "White", "Gourmand"]:
        return Simple(["Access-SL", "The Mark"])
    if options.starting_scug == "Watcher":
        return AllOf(Simple("The Mark"), Simple([f"Access-{r}" for r in watcher_pearls], 3))
    return AllOf(Simple("The Mark"), wanderer_pip_factory(3))


#################################################################
# WANDERER
# These sets are *story regions*.
regions = game_data.general.story_regions_vanilla
regions_msc = game_data.general.story_regions_msc
regions_gourmand = game_data.general.story_regions_gourmand
regions_artificer = game_data.general.story_regions_artificer
regions_rivulet = game_data.general.story_regions_rivulet
regions_spearmaster = game_data.general.story_regions_spearmaster
regions_saint = game_data.general.story_regions_saint


def generate_cond_wanderer(options: RainWorldOptions) -> Condition:
    return Simple([f"Access-{r}" for r in wanderer_regions(options.starting_scug, options.msc_enabled)])


def wanderer_regions(scug: str, msc: bool) -> set[str]:
    if not msc:
        return regions
    elif scug in ["Yellow", "White", "Red", "Inv"]:
        return regions_msc
    else:
        return {
            "Gourmand": regions_gourmand, "Artificer": regions_artificer, "Rivulet": regions_rivulet,
            "Spear": regions_spearmaster, "Saint": regions_saint, "Watcher": set()
        }[scug]


def wanderer_pip_factory(count: int) -> Condition:
    # We just need access to some number of regions from this list, it's not necessary to filter by gamestate
    return Simple([f"Access-{r}" for r in regions_all], count)


#################################################################
# LOCATIONS
locations: dict[str, LocationData] = {
    "Martyr": Passage("Martyr", "Early Passages", 5000),
    "Mother": Passage("Mother", "Early Passages", 5001, cond_mother),
    "Pilgrim": Passage("Pilgrim", "Early Passages", 5002, access_condition_generator=generate_cond_pilgrim),
    "Survivor": Passage("Survivor", "Early Passages", 5003, access_condition_generator=generate_cond_survivor),

    "DragonSlayer": Passage("DragonSlayer", "PPwS Passages", 5020,
                            access_condition_generator=generate_cond_dragonslayer),
    "Friend": Passage("Friend", "PPwS Passages", 5021, cond_friend),
    "Traveller": Passage("Traveller", "PPwS Passages", 5022, access_condition_generator=generate_cond_wanderer),

    "Chieftain": Passage("Chieftain", "Late Passages", 5040, access_condition_generator=generate_cond_chieftain),
    "Hunter": Passage("Hunter", "Late Passages", 5041, access_condition_generator=generate_cond_hunter),
    "Monk": Passage("Monk", "Late Passages", 5042, access_condition_generator=generate_cond_monk),
    "Outlaw": Passage("Outlaw", "Late Passages", 5043, access_condition_generator=generate_cond_outlaw),
    "Saint": Passage("Saint", "Late Passages", 5044, access_condition_generator=generate_cond_monk),
    "Scholar": Passage("Scholar", "Late Passages", 5045, access_condition_generator=generate_cond_scholar),
    "Nomad": Passage("Nomad", "Late Passages", 5046, access_condition_generator=generate_cond_nomad),
    **{
        f"Wanderer-{i}": LocationData(
            f"The Wanderer - {i} pip{'s' if i > 1 else ''}",
            f"Wanderer-{i}", [], 5049 + i, "PPwS Passages", wanderer_pip_factory(i)
        ) for i in range(1, 15)
    }
}


def generate(options: RainWorldOptions) -> list[LocationData]:
    keys = ["Survivor", "Friend", "Monk", "Saint"]

    if options.starting_scug != "Artificer":
        keys.append("Chieftain")

    if options.starting_scug != "Saint":
        keys += ["Hunter", "Outlaw", "DragonSlayer"]
        if (options.starting_scug != "Yellow" or options.msc_enabled) and options.starting_scug != "Inv":
            keys.append("Scholar")

    if options.msc_enabled:
        keys.append("Martyr")
        if options.starting_scug != "Watcher":
            keys += ["Pilgrim", "Nomad"]
        if options.starting_scug in ["White", "Red", "Gourmand"]:
            keys.append("Mother")

    if options.starting_scug != "Watcher":
        # Riv can't get last pip if Submerged inaccessible
        if options.starting_scug != "Rivulet" or options.submerged_should_populate:
            keys += [f"Wanderer-{i + 1}" for i in range(len(wanderer_regions(options.starting_scug, options.msc_enabled)))]
            keys.append("Traveller")
        else:
            keys += [f"Wanderer-{i + 1}" for i in range(len(wanderer_regions(options.starting_scug, options.msc_enabled)) - 1)]

    return [locations[key] for key in keys]
