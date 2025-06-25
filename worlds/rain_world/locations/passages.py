from .classes import Passage, LocationData
from .. import game_data
from ..options import RainWorldOptions
from ..conditions.classes import Condition, Simple, AnyOf, AllOf


#################################################################
# CHIEFTAIN
def generate_cond_chieftain(options: RainWorldOptions) -> Condition:
    return AllOf(
        (
            Simple("Toll") if options.difficulty_chieftain else Simple(["Scavenger", "ScavengerElite"], 1)
        ),
        Simple([f"Scug-{s}" for s in set(game_data.general.scugs_all) - {"Artificer"}], 1)
    )


#################################################################
# DRAGON SLAYER
def generate_cond_dragonslayer(options: RainWorldOptions) -> Condition:
    if not options.msc_enabled:
        return Simple(game_data.general.dragonslayer_vanilla)
    if options.difficulty_extreme_threats == 2:
        return Simple(game_data.general.dragonslayer_msc, 6)
    elif options.difficulty_extreme_threats == 1:
        return AnyOf(
            Simple(game_data.general.dragonslayer_msc.difference({"RedLizard"}), 6),
            AllOf(
                Simple(game_data.general.dragonslayer_msc, 6),
                Simple(["Scug-Artificer", "Scug-Spear", "Scug-Inv"], 1)
            )
        )
    else:
        return Simple(game_data.general.dragonslayer_msc.difference({"RedLizard"}), 6)


#################################################################
# FRIEND
cond_friend = Simple(game_data.general.lizards_any, 1)


#################################################################
# HUNTER
def generate_cond_hunter(options: RainWorldOptions) -> Condition:
    return AnyOf(
        AllOf(
            Simple(["Scug-Red", "Scug-Artificer", "Scug-Spear", "Scug-Gourmand", "Scug-Inv"], 1),
            Simple([f"Access-{region}" for region in set(game_data.general.regions_all).difference({"SS", "MS"})], 1)
        ),
        AllOf(
            Simple(["Scug-Yellow", "Scug-White", "Scug-Rivulet"], 1),
            Simple(
                ["Fly", "SmallNeedleWorm", "SmallCentipede", "Centipede",
                 "EggBug", "JellyFish", "Hazer", "VultureGrub"],
                options.difficulty_hunter.value
            )
        )
    )


#################################################################
# MONK
def generate_cond_monk(options: RainWorldOptions) -> Condition:
    if options.starting_scug in ["Spear", "Artificer", "Red"]:
        return Simple(["Access-SI", "Access-LF", "Access-SS", "Access-DM"], 1)
    return AnyOf(
        Simple(game_data.general.monk_foods_vanilla, options.difficulty_monk.value),
        AllOf(Simple('MSC'), Simple(game_data.general.monk_foods_msc, options.difficulty_monk.value))
    )


#################################################################
# MOTHER
cond_mother = AllOf(
    Simple("MSC"),
    Simple([f"Scug-{scug}" for scug in ("White", "Red", "Gourmand")], 1),
    Simple([f"Access-{region}" for region in game_data.general.slugpup_normal_regions], 1)
)


#################################################################
# NOMAD
def generate_cond_nomad(options: RainWorldOptions) -> Condition:
    return AllOf(
        Simple("MSC"),
        Simple([f"Access-{region}" for region in game_data.general.regions_all], options.difficulty_nomad.value)
    )


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
cond_scholar = AnyOf(
    Simple(["MSC", "Scug-Yellow", "Access-SL", "The Mark"]),  # Monk requires MSC to see colored pearls
    AllOf(
        Simple(["Scug-White", "Scug-Gourmand"], 1),
        Simple(["Access-SL", "The Mark"])
    ),
    AllOf(
        Simple(["Scug-Artificer", "Scug-Spear", "Scug-Red", "Scug-Rivulet"], 1),
        Simple("The Mark")
    ),
)

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

cond_wanderer_vanilla = AllOf(Simple([f"Access-{r}" for r in regions]), Simple("MSC", negative=True))
cond_wanderer_msc_base = AllOf(
    Simple([f"Access-{r}" for r in regions_msc] + ["MSC"]),
    Simple(["Scug-Yellow", "Scug-White", "Scug-Red", "Scug-Inv"], 1)
)
cond_wanderer_gourmand = Simple([f"Access-{r}" for r in regions_gourmand] + ["MSC", "Scug-Gourmand"])
cond_wanderer_artificer = Simple([f"Access-{r}" for r in regions_artificer] + ["MSC", "Scug-Artificer"])
cond_wanderer_rivulet = Simple([f"Access-{r}" for r in regions_rivulet] + ["MSC", "Scug-Rivulet"])
cond_wanderer_spearmaster = Simple([f"Access-{r}" for r in regions_spearmaster] + ["MSC", "Scug-Spear"])
cond_wanderer_saint = Simple([f"Access-{r}" for r in regions_saint] + ["MSC", "Scug-Saint"])

cond_wanderer = AnyOf(cond_wanderer_vanilla, cond_wanderer_msc_base, cond_wanderer_gourmand,
                      cond_wanderer_artificer, cond_wanderer_rivulet, cond_wanderer_spearmaster, cond_wanderer_saint)


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
    return AnyOf(
        AllOf(Simple("MSC", negative=True), Simple([f"Access-{r}" for r in regions], count)),
        AllOf(
            Simple("MSC"),
            Simple(["Scug-Yellow", "Scug-White", "Scug-Red", "Scug-Inv"], 1),
            Simple([f"Access-{r}" for r in regions_msc], count)
        ),
        AllOf(Simple("Scug-Gourmand"), Simple([f"Access-{r}" for r in regions_gourmand], count)),
        AllOf(Simple("Scug-Artificer"), Simple([f"Access-{r}" for r in regions_artificer], count)),
        AllOf(Simple("Scug-Rivulet"), Simple([f"Access-{r}" for r in regions_rivulet], count)),
        AllOf(Simple("Scug-Spear"), Simple([f"Access-{r}" for r in regions_spearmaster], count)),
        AllOf(Simple("Scug-Saint"), Simple([f"Access-{r}" for r in regions_saint], count)),
    )


#################################################################
# LOCATIONS
locations: dict[str, LocationData] = {
    "Martyr": Passage("Martyr", "Early Passages", 5000),
    "Mother": Passage("Mother", "Early Passages", 5001, cond_mother),
    "Pilgrim": Passage("Pilgrim", "Early Passages", 5002, access_condition_generator=generate_cond_pilgrim),
    "Survivor": Passage("Survivor", "Early Passages", 5003, Simple("Karma", 4)),

    "DragonSlayer": Passage("DragonSlayer", "PPwS Passages", 5020,
                            access_condition_generator=generate_cond_dragonslayer),
    "Friend": Passage("Friend", "PPwS Passages", 5021, cond_friend),
    "Traveller": Passage("Traveller", "PPwS Passages", 5022, cond_wanderer),

    "Chieftain": Passage("Chieftain", "Late Passages", 5040, access_condition_generator=generate_cond_chieftain),
    "Hunter": Passage("Hunter", "Late Passages", 5041, access_condition_generator=generate_cond_hunter),
    "Monk": Passage("Monk", "Late Passages", 5042, access_condition_generator=generate_cond_monk),
    "Outlaw": Passage("Outlaw", "Late Passages", 5043, access_condition_generator=generate_cond_outlaw),
    "Saint": Passage("Saint", "Late Passages", 5044, access_condition_generator=generate_cond_monk),
    "Scholar": Passage("Scholar", "Late Passages", 5045, cond_scholar),
    "Nomad": Passage("Nomad", "Late Passages", 5046, access_condition_generator=generate_cond_nomad),
    **{
        f"Wanderer-{i}": LocationData(
            f"The Wanderer - {i} pip{'s' if i > 1 else ''}",
            f"Wanderer-{i}", [], 5049 + i, "PPwS Passages", wanderer_pip_factory(i)
        ) for i in range(1, 15)
    }
}


def generate(options: RainWorldOptions) -> list[LocationData]:
    keys = ["Survivor", "Friend", "Traveller", "Monk", "Saint"]

    if options.starting_scug == "Watcher":
        return []

    if options.starting_scug != "Artificer":
        keys.append("Chieftain")

    if options.starting_scug != "Saint":
        keys += ["Hunter", "Outlaw", "DragonSlayer"]
        if (options.starting_scug != "Yellow" or options.msc_enabled) and options.starting_scug != "Inv":
            keys.append("Scholar")

    if options.msc_enabled:
        keys += ["Martyr", "Pilgrim", "Nomad"]
        if options.starting_scug in ["White", "Red", "Gourmand"]:
            keys.append("Mother")

    if options.starting_scug != "Watcher":
        keys += [f"Wanderer-{i+1}" for i in range(len(wanderer_regions(options.starting_scug, options.msc_enabled)))]

    return [locations[key] for key in keys]
