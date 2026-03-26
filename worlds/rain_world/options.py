from collections import Counter
from dataclasses import dataclass
from random import Random

from Options import PerGameCommonOptions, Toggle, Range, OptionGroup, Choice, ProgressionBalancing, Accessibility, \
    Visibility, DeathLinkMixin, DeathLink, FreeText, OptionList, OptionCounter, OptionError
from .conditions import GameStateFlag
from .game_data import static_data
from .game_data.bitflag import ScugFlagMap
from .game_data.general import story_regions_watcher, story_regions_vanilla, all_regions


#################################################################
# IMPORTANT SETTINGS
class PassageProgressWithoutSurvivor(Choice):
    """How The Survivor affects earning other passages.

    **Disabled**: Only The Martyr, The Mother, and The Pilgrim can be earned before The Survivor.

    **Enabled**: The Dragon Slayer, The Friend, and The Wanderer can additionally be earned before The Survivor.

    **Bypassed**: Every passage can be earned before The Survivor.

    This will override the actual value of the corresponding setting in the Rain World Remix menu."""
    display_name = "Passage progress without Survivor"
    option_disabled = 0
    option_enabled = 1
    option_bypassed = 2

    default = 2


class IsMSCEnabled(Toggle):
    """Whether More Slugcats Expansion (Downpour) is enabled, regardless of which campaign you plan to play."""
    display_name = "More Slugcats Expansion?"
    default = 0


class IsWatcherEnabled(Toggle):
    """Whether The Watcher is enabled, regardless of which campaign you plan to play."""
    display_name = "The Watcher?"
    default = 0


class WhichGameVersion(Choice):
    """Which Rain World version you are using."""
    display_name = "Game version"
    option_1_9_15b = 1091503
    alias_1_9_15_3 = 1091503
    alias_1_9_15 = 1091503
    alias_1_9 = 1091503
    option_1_10_4 = 1100400
    alias_1_10 = 1100400
    alias_1_10_1 = 1100400
    alias_1_10_2 = 1100400
    alias_1_10_3 = 1100400
    default = 1100400

    displaying = {
        1091503: ("v1.9.15b / v1.9.15.3", "1.9.15.3"),
        1100400: ("v1.10.0 - v1.11.1", "1.11.6"),
    }

    @property
    def string(self) -> str: return self.displaying[self.value][1]

    @classmethod
    def get_option_name(cls, value: int) -> str: return cls.displaying[value][0]

    visibility = Visibility.none


class WhichCampaign(Choice):
    """Which slugcat's campaign you will play."""
    display_name = "Campaign"
    option_monk = 0
    option_survivor = 1
    option_hunter = 2
    option_gourmand = 3
    option_artificer = 4
    option_rivulet = 5
    option_spearmaster = 6
    option_saint = 7
    option_sofanthiel = 8
    option_watcher = 9

    alias_yellow = 0
    alias_white = 1
    alias_red = 2
    alais_gourm = 3
    alias_arti = 4
    alias_riv = 5
    alias_spear = 6
    alias_sait = 7
    alias_inv = 8
    alias_enot = 8

    default = 1

    ids_names = {
        0: ("Yellow", "Monk"),
        1: ("White", "Survivor"),
        2: ("Red", "Hunter"),
        3: ("Gourmand", "Gourmand"),
        4: ("Artificer", "Artificer"),
        5: ("Rivulet", "Rivulet"),
        6: ("Spear", "Spearmaster"),
        7: ("Saint", "Saint"),
        8: ("Inv", "Sofanthiel"),
        9: ("Watcher", "Watcher"),
    }

    @property
    def scug_id(self) -> str:
        return self.__class__.ids_names[self.value][0]

    @property
    def scug_name(self) -> str:
        return self.__class__.ids_names[self.value][1]


class WhichVictoryCondition(Choice):
    """What the victory condition should be.
    **Ascension** is the default, and **Story** is the slugcat specific ending.
    **Echoes** requires meeting enough Echoes to satisfy the Pilgrim passage.
    **Food Quest** requires eating every edible food in order to fill out the tracker.
    This includes expanded food quest, if it is enabled.

    The **Story** victory condition depends on the selected gamestate:

    **Vanilla**, **Saint**, or **Sofanthiel**: No alternate.

    **Monk** and **Survivor**: Reach Journey's End in Outer Expanse.

    **Hunter**: Use the green neuron on Looks to the Moon in Shoreline.

    **Gourmand**: Receive the Mark in order to reach Outer Expanse, and subsequently reach Journey's End.

    **Artificer**: Receive the Mark and the Citizen ID drone in order to reach Metropolis and kill the Chieftain Scavenger.

    **Rivulet**: Receive the Rarefaction Cell and deliver it to Submerged Superstructure,
    then meet Looks to the Moon.

    **Spearmaster**: Receive the SM pearl and Moon's message, then deliver it to Communications Array in Sky Islands.

    When playing as the Watcher, these options are different:
    **Ascension** / **Spinning Top**: Complete the Spinning Top ending.
    **Story** / **Prince**: Complete the Prince ending.
    **Weaver**: Complete the Weaver ending.
    **True Ending**: Complete the True ending.
    """
    display_name = "Victory condition"
    option_ascension = 0
    option_story = 1
    option_echoes = 2
    option_food_quest = 3

    alias_spinning_top = 0
    alias_prince = 1
    option_weaver = 4
    option_true_ending = 5


class WhichGateBehavior(Choice):
    """
    **Key only**: A key for each accessible gate is placed into the pool.
    These keys are required to use karma gates, and karma is not.

    **Key and Karma**: Keys are required *and* gates have karma requirements.

    **Key or Karma**: Either keys or karma are sufficient to use a gate.

    **Karma only**: Unrandomized behavior.  Keys are not placed into the pool.

    Gates will have Monk-style behavior if you choose a setting other than **Key only**.
    """
    display_name = "Gate behavior"
    option_key_only = 0
    option_key_and_karma = 1
    option_key_or_karma = 2
    option_karma_only = 3
    default = 0


class DebugOutput(Toggle):
    """Whether to log extra information about the world and slot for debugging."""
    default = False
    visibility = Visibility.none


#################################################################
# WATCHER SETTINGS
class RippleWarpBehavior(Choice):
    """How ripple warps behave.  See the settings documentation for explanation."""
    display_name = "Ripple warp behavior"
    option_unaltered = 0
    option_no_ripple_warps = 1
    alias_true = 1
    alias_false = 0
    default = 0
    # visibility = Visibility.none


class NormalDynamicWarpBehavior(Choice):
    """How normal dynamic warps behave.  See the Watcher documentation for explanation."""
    display_name = "Normal dynamic warp behavior"
    option_ignored = 0
    option_visited = 1
    option_static_pool = 2
    option_unlockable_pool = 4
    option_static_predetermined = 5
    option_unlockable_predetermined = 6
    default = 1
    visibility = Visibility.none

    @property
    def unlockable(self) -> bool: return self.value in (4, 6)

    @property
    def predetermined(self) -> bool: return self.value in (5, 6)


class PredeterminedDynamicWarpNetworkMinimumNecklaceLength(Range):
    """The minimum length of a necklace in the derangement generator for the predetermined dynamic warp network."""
    display_name = "Warp network parameter"
    range_start = 2
    range_end = 18
    default = 3
    visibility = Visibility.none


class ThroneDynamicWarpBehavior(Choice):
    """How Throne dynamic warps behave.  See the Watcher documentation for explanation."""
    display_name = "Throne dynamic warp behavior"
    option_ignored = 0
    option_visited = 1
    option_static_predetermined = 5
    default = 5
    visibility = Visibility.none


class DynamicWarpPoolSize(Range):
    """Number of regions in the dynamic warp pool.  See the Watcher documentation for explanation."""
    display_name = "Normal pool size"
    range_start = 1
    range_end = 18
    default = 18
    visibility = Visibility.none


class LogicRottedGeneration(Choice):
    """Controls the generation of Crumbling Fringes, Corrupted Factories, Decaying Tunnels, and Infested Wastes.

    **None**: There will be no checks in rotted vanilla regions, and bad warping will not be required to reach Outer Rim.

    **Passthrough**: There will be no checks in rotted vanilla regions, but you may still have to bad warp to reach Outer Rim.

    **Full**: Checks will be present in rotted vanilla regions
    """
    display_name = "Permarotted accessibility"
    option_none = 0
    option_passthrough = 1
    option_full = 2
    alias_true = 2
    alias_false = 0
    default = 1
    # visibility = Visibility.none


class LogicMinRippleTarget(Range):
    """The lowest that your *minimum* Ripple can be before Ripplespace is logically accessible.
    The default, 5, matches the actual game behavior."""
    display_name = "Min Ripple target"
    range_start = 5
    range_end = 9
    default = 5
    # visibility = Visibility.none


class RottedRegionTarget(Range):
    """The number of regions that must be rotted for the Rot ending.
    The default, 21, matches the unaltered game behavior."""
    display_name = "Rotted region target"
    range_start = 2
    range_end = 21
    default = 21
    # visibility = Visibility.none


class ChecksSpreadRot(Choice):
    """Whether spreading the Rot to a new region is a check.
    When Weaver or True ending is chosen, rot checks will not generate regardless of chosen value"""
    display_name = "Rot spread checks"
    option_off = 0
    option_prince_ending_only = 1
    option_on = 2
    alias_true = 2
    alias_false = 0
    default = 1
    # visibility = Visibility.none


class SpinningTopKeys(Toggle):
    """Whether keys are required to travel through Spinning Top warps."""
    display_name = "Spinning Top keys"
    default = True
    # visibility = Visibility.none


class DaemonKeys(Toggle):
    """Whether keys are required to travel through Daemon warps."""
    display_name = "Daemon keys"
    default = False


class PriorityThrone(Choice):
    """Whether Prince checks should be normal, priority, or excluded locations."""
    display_name = "Priority Throne"
    option_normal = 1
    option_priority = 2
    option_excluded = 3
    default = 1
    # visibility = Visibility.none


class UseWatcherPassages(Toggle):
    """Whether passage tokens will be added to the item pool when playing as Watcher.
    You will need the mod "Watcher Region Art" enabled in order to use passage tokens in-game.
    The mod can be found on the Steam workshop: https://steamcommunity.com/sharedfiles/filedetails/?id=3660768308
    """
    display_name = "Use Watcher Passages"
    default = False


#################################################################
# GENERAL SETTINGS
class RandomStartingRegion(Choice):
    """Whether the starting region should be randomized.

    **Default Start**: Do not randomize the starting region.

    **Weighted Choice**: Refer to "Possible Starting Regions" option to decide what starting regions can be chosen.

    **Any Valid**: The starting region is chosen among every accessible region in the selected game state.
    """
    display_name = "Randomize Starting Region"

    option_default_start = 0
    option_weighted_choice = 1
    option_any_valid = 2

    default = 0


class PossibleStartingRegions(OptionCounter):
    """Select which regions will be allowed as possible starting locations.
    Only used when "Randomize Starting Region" option is set to "Weighted Choice".
    The value on each region influences how likely it is to be selected.
    Regions not in the list or with a value less than 1 are not selected.
    """
    display_name = "Possible Starting Regions"

    resolved_name: str
    resolved_code: str

    names = {
        "Outskirts": "SU",
        "Industrial Complex": "HI",
        "Drainage System / Undergrowth": "DS",
        "Garbage Wastes": "GW",
        "Shoreline / Waterfront Facility": "SL",
        "Shaded Citadel / Silent Construct": "SH",
        "The Exterior": "UW",
        "Five Pebbles / The Rot": "SS",
        "Chimney Canopy": "CC",
        "Sky Islands": "SI",
        "Farm Arrays": "LF",
        "Subterranean": "SB",

        "Pipeyard": "VS",
        "Submerged Superstructure": "MS",
        "Outer Expanse": "OE",
        "Metropolis": "LC",
        "Looks to the Moon": "DM",

        "Sunbaked Alley": "WSKB",
        "Coral Caves": "WRFA",
        "Torrential Railways": "WSKA",
        "Aether Ridge": "WARF",
        "Badlands": "WBLA",
        "Cold Storage": "WARD",
        "Desolate Tract": "WTDB",
        "Fetid Glen": "WARC",
        "Fractured Gateways": "WVWB",
        "Heat Ducts": "WARE",
        "Migration Path": "WMPA",
        "Pillar Grove": "WPGA",
        "Rusted Wrecks": "WRRA",
        "Salination": "WARB",
        "Shrouded Stacks": "WSKD",
        "Signal Spires": "WPTA",
        "Stormy Coast": "WSKC",
        "The Surface": "WARG",
        "Torrid Desert": "WTDA",
        "Turbulent Pump": "WRFB",
        "Verdant Waterways": "WVWA",
    }

    default = {name: 1 for name in names.keys()}


class PassagePriority(Range):
    """Number of Passages that are randomly marked as priority checks,
    increasing the chance that they will contain progression items.
    These are in addition to any manually-prioritized Passages,
    and will not override any manually-excluded Passages."""
    display_name = "Priority Passages"
    range_start = 0
    range_end = 14
    default = 3


class ExtraKarmaCapIncreases(Range):
    """Number of extra karma cap increases in the pool beyond the minimum required for ascension.
    For Watcher, this option will also apply to Ripple."""
    display_name = "Extra karma cap increases"
    range_start = 0
    range_end = 30
    default = 3


#################################################################
# CHECK POOL SETTINGS
class ChecksBroadcasts(Choice):
    """Which slugcats broadcasts should be available to.  Requires MSC."""
    display_name = "Broadcasts"
    option_all_slugcats = 2
    option_only_spearmaster = 1
    option_off = 0
    alias_true = 2
    alias_false = 0
    default = 1
    visibility = Visibility.none


class ChecksFoodQuest(Choice):
    """Which slugcats the food quest should be available to.  Requires MSC."""
    display_name = "Food quest"
    option_all_slugcats = 2
    option_only_gourmand = 1
    option_off = 0
    alias_true = 2
    alias_false = 0
    default = 2


class ChecksFoodQuestExpanded(Toggle):
    """Whether the food quest should be expanded to include most creatures.
    Specific food quest checks may be disabled by excluding the locations,
    and some slugcats will not be required to kill and eat extreme threats if that setting is enabled.
    Requires MSC."""
    display_name = "Expanded food quest"
    default = False


class ChecksTokensPearls(Toggle):
    """Whether all tokens and pearls should be visible to all slugcats."""
    display_name = "All tokens and pearls"
    default = False
    visibility = Visibility.none


class ChecksDevTokens(Toggle):
    """Whether dev commentary tokens should be checks.  Requires MSC."""
    display_name = "Dev tokens"
    default = False


class ChecksSheltersanity(Toggle):
    """Whether each shelter is a check."""
    display_name = "Sheltersanity"
    default = False


class ChecksSubmerged(Choice):
    """Whether Submerged Superstructure has any checks.
    If only aquatic is chosen, checks will only be generated
    if playing Rivulet or the Aquatic perk is in the item pool."""
    display_name = "Include Submerged"
    option_all_slugcats = 2
    option_only_aquatic = 1
    option_off = 0

    alias_true = 2
    alias_false = 0
    alias_only_rivulet = 1

    default = 1


class ChecksKarmaFlowers(Toggle):
    """Whether each static karma flower spawn is a check."""
    display_name = "Karma Flowers"
    default = False


#################################################################
# DIFFICULTY SETTINGS
class DifficultyHunter(Range):
    """The number of different types of meats that must be available before The Hunter can be logically required.
    Higher numbers are easier."""
    display_name = "The Hunter difficulty"
    range_start = 1
    range_end = 4
    default = 3


class DifficultyMonk(Range):
    """The number of different types of non-meats that must be available before The Monk can be logically required.
    Higher numbers are easier."""
    display_name = "The Monk difficulty"
    range_start = 1
    range_end = 4
    default = 3


class DifficultyOutlaw(Range):
    """The number of different types of creatures that must be available before The Outlaw can be logically required.
    Higher numbers are easier."""
    display_name = "The Outlaw difficulty"
    range_start = 1
    range_end = 8
    default = 5


class DifficultyNomad(Range):
    """The number of regions that must be accessible before The Nomad can be logically required.
    Higher numbers are easier."""
    display_name = "The Nomad difficulty"
    range_start = 3
    range_end = 8
    default = 5


class DifficultyChieftain(Toggle):
    """Whether a Scavenger toll must be accessible before The Chieftain can be logically required.
    If disabled, Chieftain becomes accessible whenever any Scavengers are accessible."""
    display_name = "The Chieftain requires toll"
    default = True


class DifficultyGlow(Toggle):
    """Whether the neuron glow is logically required for Shaded Citadel,
    parts of lower Pipeyard, and Filtration System."""
    display_name = "Glow required for dark places"
    default = True


class DifficultyExtremeThreats(Toggle):
    """Whether eliminating an extreme threat could be required (such as for a food quest check).
    This includes Daddy Long Legs (and variants), Red Lizards, King Vultures, Miros Vultures,
    Miros Birds, Aquapedes, and Red Centipedes."""
    display_name = "Extreme threats"
    default = 0


class DifficultySubmerged(Choice):
    """Changes the logical requirement for entering Submerged Superstructure.

    If off, Submerged has no additional requirement to enter.

    If set to aquatic, access to Submerged will expect you to have longer breath time from the Aquatic perk
    or to be playing as Rivulet. If the Aquatic perk is not in the item pool, this acts the same as "off".

    If set to longer cycles, Rivulet will not be expected to enter Submerged until the Longer Cycles item is obtained."""
    display_name = "Late Submerged"
    option_longer_cycles = 2
    option_aquatic = 1
    option_off = 0

    alias_true = 2
    alias_false = 0
    alias_only_rivulet = 2

    default = 1


class DifficultyEchoLowKarma(Choice):
    """How echo apperances work below 5 max karma.
    Does not affect the echoes in Subterranean and The Exterior, which can always be visited.

    **Unaltered**: Vanilla behavior.  Artificer needs a karma flower and other slugcats do not.

    **Never**: Echoes cannot appear below 5 karma.

    **With Karma Flower**: Echoes may appear below 5 karma
    if karma flower reinforcement is active and current karma equals max karma.
    This is the normal behavior for Artificer.

    **Without Karma Flower**: Echoes may appear if current karma equals max karma."""
    display_name = "Low-karma echo appearance"
    option_never = 0
    option_with_karma_flower = 1
    option_without_karma_flower = 2
    option_unaltered = 3
    default = 3

#################################################################
# UPGRADE SETTINGS
class UpgradesSpearDamage(Range):
    """Add an amount of items to the pool that permanently increase the damage of thrown spears.
    Each progressive upgrade adds 10% damage on top of the slugcat's base damage."""
    display_name = "Spear damage increases"
    range_start = 0
    range_end = 10
    default = 6

#################################################################
# FILLER SETTINGS
class ExpeditionPerks(OptionList):
    """Choose which Expedition perks will be added to the item pool.
    If an ability in this list is given to a slugcat that innately has it, there is no effect.
    Requires MSC.

    Valid Perks: Back Spear Perk, Dual Wielding Perk, Blast Resistance Perk, Explosive Parry Perk,
    Explosive Jump Perk, Crafting Perk, Aquatic Perk, Agility Perk"""
    display_name = "Expedition Perks"
    valid_keys = ["Back Spear Perk", "Dual Wielding Perk", "Blast Resistance Perk", "Explosive Parry Perk",
                  "Explosive Jump Perk", "Crafting Perk", "Aquatic Perk", "Agility Perk"]
    verify_item_name = True


class PctTraps(Range):
    """The percentage of filler items that will be traps.  Set to 0 to remove traps entirely."""
    display_name = "Trap percentage"
    range_start = 0
    range_end = 100
    default = 30


class FillerJitter(Range):
    """Each non-zero filler weight receives a random number, up to this jitter value, added to it.
    The lower the setting, the less likely it is that items with small weights appear in the pool at all.
    The higher the setting, the lower the influence of the item weights altogether."""
    display_name = "Filler weight jitter"
    range_start = 0
    range_end = 100
    default = 10


class WtGeneric(Range):
    range_start = 0
    range_end = 100


class WtRock(WtGeneric):
    """The relative weight of rocks in the non-trap filler item pool."""
    display_name = "Rock"
    item_name = "Rock"
    default = 100


class WtSpear(WtGeneric):
    """The relative weight of spears in the non-trap filler item pool."""
    display_name = "Spear"
    item_name = "Spear"
    default = 40


class WtExplosiveSpear(WtGeneric):
    """The relative weight of explosive spears in the non-trap filler item pool."""
    display_name = "Explosive Spear"
    item_name = "Explosive Spear"
    default = 10


class WtGrenade(WtGeneric):
    """The relative weight of grenades in the non-trap filler item pool."""
    display_name = "Grenade"
    item_name = "Grenade"
    default = 10


class WtFlashbang(WtGeneric):
    """The relative weight of flashbangs in the non-trap filler item pool."""
    display_name = "Flashbang"
    item_name = "Flashbang"
    default = 20


class WtSporePuff(WtGeneric):
    """The relative weight of spore puffs in the non-trap filler item pool."""
    display_name = "Spore Puff"
    item_name = "Spore Puff"
    default = 20


class WtCherrybomb(WtGeneric):
    """The relative weight of cherrybombs in the non-trap filler item pool."""
    display_name = "Cherrybomb"
    item_name = "Cherrybomb"
    default = 30


class WtBubbleWeed(WtGeneric):
    """The relative weight of bubble weed in the non-trap filler item pool."""
    display_name = "Bubble Weed"
    item_name = "Bubble Weed"
    default = 20


class WtLillyPuck(WtGeneric):
    """The relative weight of lilypucks in the non-trap filler item pool."""
    display_name = "Lilypuck (MSC)"
    item_name = "Lilypuck"
    default = 20


class WtDandelionPeach(WtGeneric):
    """The relative weight of dandelion peaches in the non-trap filler item pool."""
    display_name = "Dandelion Peach (MSC)"
    item_name = "Dandelion Peach"
    default = 20


class WtGooieduck(WtGeneric):
    """The relative weight of gooieducks in the non-trap filler item pool."""
    display_name = "Gooieduck (MSC)"
    item_name = "Gooieduck"
    default = 20


class WtFruit(WtGeneric):
    """The relative weight of blue fruit in the non-trap filler item pool."""
    display_name = "Blue Fruit"
    item_name = "Blue Fruit"
    default = 60


class WtBubbleFruit(WtGeneric):
    """The relative weight of bubble fruit in the non-trap filler item pool."""
    display_name = "Bubble Fruit"
    item_name = "Bubble Fruit"
    default = 40


class WtEggbugEgg(WtGeneric):
    """The relative weight of eggbug eggs in the non-trap filler item pool."""
    display_name = "Eggbug Egg"
    item_name = "Eggbug Egg"
    default = 30


class WtJellyfish(WtGeneric):
    """The relative weight of jellyfish in the non-trap filler item pool."""
    display_name = "Jellyfish"
    item_name = "Jellyfish"
    default = 15


class WtMushroom(WtGeneric):
    """The relative weight of mushrooms in the non-trap filler item pool."""
    display_name = "Mushroom"
    item_name = "Mushroom"
    default = 15


class WtSlimeMold(WtGeneric):
    """The relative weight of slime mold in the non-trap filler item pool."""
    display_name = "Slime Mold"
    item_name = "Slime Mold"
    default = 35


class WtFireEgg(WtGeneric):
    """The relative weight of firebug eggs in the non-trap filler item pool."""
    display_name = "Firebug egg (MSC)"
    item_name = "Fire Egg"
    default = 5


class WtGlowWeed(WtGeneric):
    """The relative weight of glow weed in the non-trap filler item pool."""
    display_name = "Glow Weed (MSC)"
    item_name = "Glow Weed"
    default = 15


class WtElectricSpear(WtGeneric):
    """The relative weight of electric spears in the non-trap filler item pool."""
    display_name = "Electric Spear (MSC)"
    item_name = "Electric Spear"
    default = 3


class WtSingularityBomb(WtGeneric):
    """The relative weight of singularity bombs in the non-trap filler item pool."""
    display_name = "Singularity Bomb (MSC)"
    item_name = "Singularity Bomb"
    default = 1


class WtLantern(WtGeneric):
    """The relative weight of lanterns in the non-trap filler item pool."""
    display_name = "Lantern"
    item_name = "Lantern"
    default = 15


class WtKarmaFlower(WtGeneric):
    """The relative weight of karma flowers in the non-trap filler item pool."""
    display_name = "Karma Flower"
    item_name = "Karma Flower"
    default = 5


class WtVultureMask(WtGeneric):
    """The relative weight of vulture masks in the non-trap filler item pool."""
    display_name = "Vulture Mask"
    item_name = "Vulture Mask"
    default = 9


class WtPearl(WtGeneric):
    """The relative weight of pearls in the non-trap filler item pool."""
    display_name = "Pearl"
    item_name = "Pearl"
    default = 9


class WtBeehive(WtGeneric):
    """The relative weight of beehives in the non-trap filler item pool."""
    display_name = "Beehive"
    item_name = "Beehive"
    default = 15


class WtJokeRifle(WtGeneric):
    """The relative weight of joke rifles in the non-trap filler item pool."""
    display_name = "Joke Rifle (MSC)"
    item_name = "Joke Rifle"
    default = 1


class WtBoomerang(WtGeneric):
    """The relative weight of boomerangs in the non-trap filler item pool."""
    display_name = "Boomerang (Watcher)"
    item_name = "Boomerang"
    default = 20


class WtPoisonSpear(WtGeneric):
    """The relative weight of poison spears in the non-trap filler item pool."""
    display_name = "Poison Spear (Watcher)"
    item_name = "Poison Spear"
    default = 15


class WtGraffitiBomb(WtGeneric):
    """The relative weight of graffiti bombs in the non-trap filler item pool."""
    display_name = "Graffiti Bomb (Watcher)"
    item_name = "Graffiti Bomb"
    default = 20


class WtRotFruit(WtGeneric):
    """The relative weight of rot fruits in the non-trap filler item pool."""
    display_name = "Rot Fruit (Watcher)"
    item_name = "Rot Fruit"
    default = 0


class WtFireSpriteLarva(WtGeneric):
    """The relative weight of fire sprite larvae in the non-trap filler item pool."""
    display_name = "Fire Sprite Larva (Watcher)"
    item_name = "Fire Sprite Larva"
    default = 30


#################################################################
# TRAP SETTINGS
class WtTrapStun(WtGeneric):
    """The relative weight of stun traps in the trap filler item pool.
    Stun traps will briefly stun the slugcat, as if they were hit with a rock."""
    display_name = "Stun trap"
    item_name = "Stun trap"
    default = 60


class WtTrapZoomies(WtGeneric):
    """The relative weight of zoomies traps in the trap filler item pool.
    Zoomies traps will make the slugcat update at double speed for a short time.
    This will increase movement speed, but make platforming more difficult."""
    display_name = "Zoomies trap"
    item_name = "Zoomies trap"
    default = 50


class WtTrapTimer(WtGeneric):
    """The relative weight of timer traps in the trap filler item pool.
    Timer traps will reduce the remaining time left in the current cycle."""
    display_name = "Timer trap"
    item_name = "Timer trap"
    default = 50


class WtTrapRedLizard(WtGeneric):
    """The relative weight of red lizard traps in the trap filler item pool.
    Red lizard traps will spawn a red lizard in an adjacent room.
    It will also know the slugcat's position for a short time."""
    display_name = "Red Lizard trap"
    item_name = "Red Lizard trap"
    default = 30


class WtTrapRedCentipede(WtGeneric):
    """The relative weight of red centipede traps in the trap filler item pool.
    Red centipede traps will spawn a red centipede in an adjacent room.
    It will also know the slugcat's position for a short time."""
    display_name = "Red Centipede trap"
    item_name = "Red Centipede trap"
    default = 30


class WtTrapSpitterSpider(WtGeneric):
    """The relative weight of spitter spider traps in the trap filler item pool.
    Spitter spider traps will spawn multiple spitter spiders in an adjacent room(s).
    They will also know the slugcat's position for a short time."""
    display_name = "Spitter Spider trap"
    item_name = "Spitter Spider trap"
    default = 30


class WtTrapBrotherLongLegs(WtGeneric):
    """The relative weight of brother long legs traps in the trap filler item pool.
    Brother long legs traps will spawn multiple BLLs in an adjacent room(s).
    They will also know the slugcat's position for a short time."""
    display_name = "Brother Long Legs trap"
    item_name = "Brother Long Legs trap"
    default = 30


class WtTrapDaddyLongLegs(WtGeneric):
    """The relative weight of daddy long legs traps in the trap filler item pool.
    Daddy long legs traps will spawn a Daddy long legs in an adjacent room.
    It will also know the slugcat's position for a short time."""
    display_name = "Daddy Long Legs trap"
    item_name = "Daddy Long Legs trap"
    default = 10


class WtTrapRain(WtGeneric):
    """The relative weight of rain traps in the trap filler item pool.
    Rain traps will activate strong pre-cycle rain for a short time.
    If MSC is not enabled, this effect will only be visual."""
    display_name = "Rain trap"
    item_name = "Rain trap"
    default = 50


class WtTrapGravity(WtGeneric):
    """The relative *weight* of gravity traps in the trap filler item pool.
    Gravity traps will disable gravity for a short time.
    This has no effect in rooms with gravity effects already present (For example, in Five Pebbles)."""
    display_name = "Gravity trap"
    item_name = "Gravity trap"
    default = 10


class WtTrapFog(WtGeneric):
    """The relative weight of fog traps in the trap filler item pool."""
    display_name = "Fog trap"
    item_name = "Fog trap"
    default = 0
    visibility = Visibility.none


class WtTrapKillSquad(WtGeneric):
    """The relative weight of kill squad traps in the trap filler item pool."""
    display_name = "Killsquad trap"
    item_name = "Killsquad trap"
    default = 0
    visibility = Visibility.none


class WtTrapAlarm(WtGeneric):
    """The relative weight of alarm traps in the trap filler item pool.
    Alarm traps will alert every creature in the region to the slugcats position for some time."""
    display_name = "Alarm trap"
    item_name = "Alarm trap"
    default = 30

class WtTrapResponsibility(WtGeneric):
    """The relative weight of responsibility traps in the trap filler item pool.
    Responsibility traps will spawn a slugpup in an adjacent room.
    It will also know the slugcat's position for a short time."""
    display_name = "Responsibility trap"
    item_name = "Responsibility trap"
    default = 30

class WtTrapRippleSpawn(WtGeneric):
    """The relative weight of ripple spawn traps in the trap filler item pool.
    Ripple spawn traps will spawn a large amount of Ripple amoeba in the current room that chase the slugcat.
    Before the Glow is obtained these will be invisible, making them much more dangerous."""
    display_name = "Ripple Spawn trap"
    item_name = "Ripple Spawn trap"
    default = 0

class WtTrapBlizzardLizard(WtGeneric):
    """The relative weight of blizzard lizard traps in the trap filler item pool.
    Blizzard Lizard traps will spawn a blizzard lizard in an adjacent room.
    It will also know the slugcat's position for a short time."""
    display_name = "Blizzard Lizard trap"
    item_name = "Blizzard Lizard trap"
    default = 10


@dataclass
class RainWorldOptions(PerGameCommonOptions, DeathLinkMixin):
    starting_region_name = ""
    starting_region_code = ""

    #################################################################
    # IMPORTANT SETTINGS
    which_game_version: WhichGameVersion
    is_msc_enabled: IsMSCEnabled
    is_watcher_enabled: IsWatcherEnabled
    which_campaign: WhichCampaign
    passage_progress_without_survivor: PassageProgressWithoutSurvivor
    which_victory_condition: WhichVictoryCondition
    which_gate_behavior: WhichGateBehavior
    randomize_starting_region: RandomStartingRegion
    possible_starting_regions: PossibleStartingRegions
    debug_output: DebugOutput

    group_important = [
        WhichGameVersion, IsMSCEnabled, IsWatcherEnabled, WhichCampaign, PassageProgressWithoutSurvivor,
        WhichVictoryCondition, WhichGateBehavior, DeathLink, RandomStartingRegion, PossibleStartingRegions, DebugOutput
    ]

    #################################################################
    # DIFFICULTY SETTINGS
    difficulty_monk: DifficultyMonk
    difficulty_hunter: DifficultyHunter
    difficulty_outlaw: DifficultyOutlaw
    difficulty_nomad: DifficultyNomad
    difficulty_chieftain: DifficultyChieftain
    difficulty_glow: DifficultyGlow
    difficulty_extreme_threats: DifficultyExtremeThreats
    difficulty_submerged: DifficultySubmerged
    difficulty_echo_low_karma: DifficultyEchoLowKarma

    group_difficulty = [
        ProgressionBalancing, Accessibility, DifficultyMonk, DifficultyHunter, DifficultyOutlaw, DifficultyNomad,
        DifficultyChieftain, DifficultyGlow, DifficultyExtremeThreats, DifficultySubmerged, DifficultyEchoLowKarma,
    ]

    #################################################################
    # ITEM POOL SETTINGS
    expedition_perks: ExpeditionPerks
    pct_traps: PctTraps
    weight_jitter: FillerJitter
    extra_karma_cap_increases: ExtraKarmaCapIncreases
    damage_upgrades: UpgradesSpearDamage

    group_itempool = [
        ExtraKarmaCapIncreases, UpgradesSpearDamage, ExpeditionPerks, PctTraps, FillerJitter
    ]

    #################################################################
    # CHECK POOL SETTINGS
    checks_broadcasts: ChecksBroadcasts
    checks_foodquest: ChecksFoodQuest
    checks_foodquest_expanded: ChecksFoodQuestExpanded
    passage_priority: PassagePriority
    checks_tokens_pearls: ChecksTokensPearls
    checks_sheltersanity: ChecksSheltersanity
    checks_submerged: ChecksSubmerged
    checks_flowersanity: ChecksKarmaFlowers
    checks_devtokens: ChecksDevTokens

    group_checkpool = [
        ChecksBroadcasts, ChecksFoodQuest, ChecksFoodQuestExpanded, PassagePriority, ChecksTokensPearls,
        ChecksDevTokens, ChecksSheltersanity, ChecksSubmerged, ChecksKarmaFlowers,
    ]

    #################################################################
    # WATCHER-SPECIFIC SETTINGS
    logic_rotted_generation: LogicRottedGeneration
    logic_ripplespace_min_req: LogicMinRippleTarget
    normal_dynamic_warp_behavior: NormalDynamicWarpBehavior
    throne_dynamic_warp_behavior: ThroneDynamicWarpBehavior
    predetermined_dynamic_warp_network_minimum_necklace_length: PredeterminedDynamicWarpNetworkMinimumNecklaceLength
    dynamic_warp_pool_size: DynamicWarpPoolSize
    rotted_region_target: RottedRegionTarget
    checks_spread_rot: ChecksSpreadRot
    spinning_top_keys: SpinningTopKeys
    daemon_keys: DaemonKeys
    priority_throne: PriorityThrone
    watcher_passages: UseWatcherPassages

    group_watcher = [
        LogicRottedGeneration, LogicMinRippleTarget, NormalDynamicWarpBehavior, ThroneDynamicWarpBehavior,
        DynamicWarpPoolSize, RottedRegionTarget, ChecksSpreadRot, SpinningTopKeys, DaemonKeys,
        PriorityThrone, UseWatcherPassages, PredeterminedDynamicWarpNetworkMinimumNecklaceLength,
    ]

    #################################################################
    # FILLER SETTINGS
    wt_rocks: WtRock
    wt_spears: WtSpear
    wt_explosive_spears: WtExplosiveSpear
    wt_grenades: WtGrenade
    wt_flashbangs: WtFlashbang
    wt_sporepuffs: WtSporePuff
    wt_cherrybombs: WtCherrybomb
    wt_bubble_weed: WtBubbleWeed
    wt_lanterns: WtLantern
    wt_vulture_masks: WtVultureMask
    wt_pearls: WtPearl
    wt_beehives: WtBeehive
    wt_lilypucks: WtLillyPuck
    wt_dandelion_peaches: WtDandelionPeach
    wt_gooieducks: WtGooieduck
    wt_electric_spears: WtElectricSpear
    wt_singularity_bombs: WtSingularityBomb
    wt_joke_rifles: WtJokeRifle
    wt_boomerangs: WtBoomerang
    wt_poison_spears: WtPoisonSpear
    wt_graffiti_bombs: WtGraffitiBomb

    wt_fruit: WtFruit
    wt_bubblefruit: WtBubbleFruit
    wt_eggbugeggs: WtEggbugEgg
    wt_jellyfish: WtJellyfish
    wt_mushrooms: WtMushroom
    wt_slimemold: WtSlimeMold
    wt_karma_flowers: WtKarmaFlower
    wt_fireeggs: WtFireEgg
    wt_glowweed: WtGlowWeed
    wt_rot_fruit: WtRotFruit
    wt_fire_sprite_larva: WtFireSpriteLarva

    group_filler = [
        WtRock, WtSpear, WtExplosiveSpear, WtGrenade, WtFlashbang, WtSporePuff, WtCherrybomb, WtBubbleWeed, WtLantern,
        WtVultureMask, WtPearl, WtBeehive, WtFruit, WtBubbleFruit, WtEggbugEgg, WtJellyfish, WtMushroom, WtSlimeMold,
        WtKarmaFlower,

        WtLillyPuck, WtDandelionPeach, WtGooieduck, WtElectricSpear, WtSingularityBomb, WtJokeRifle,
        WtFireEgg, WtGlowWeed,

        WtBoomerang, WtPoisonSpear, WtGraffitiBomb, WtRotFruit, WtFireSpriteLarva
    ]

    #################################################################
    # TRAP SETTINGS

    wt_stuns: WtTrapStun
    wt_zoomies: WtTrapZoomies
    wt_timers: WtTrapTimer
    wt_killsquads: WtTrapKillSquad
    wt_alarms: WtTrapAlarm
    wt_fogs: WtTrapFog
    wt_rains: WtTrapRain
    wt_gravity: WtTrapGravity

    wt_redlizard: WtTrapRedLizard
    wt_redcentipede: WtTrapRedCentipede
    wt_spitterspider: WtTrapSpitterSpider
    wt_brotherlonglegs: WtTrapBrotherLongLegs
    wt_daddylonglegs: WtTrapDaddyLongLegs
    wt_responsibility: WtTrapResponsibility
    wt_ripplespawn: WtTrapRippleSpawn
    wt_blizzardlizard: WtTrapBlizzardLizard

    group_traps = [
        WtTrapStun, WtTrapZoomies, WtTrapTimer, WtTrapAlarm, WtTrapKillSquad,
        WtTrapGravity, WtTrapRain, WtTrapFog,

        WtTrapRedLizard, WtTrapRedCentipede, WtTrapSpitterSpider,
        WtTrapBrotherLongLegs, WtTrapDaddyLongLegs, WtTrapResponsibility,
        WtTrapRippleSpawn, WtTrapBlizzardLizard
    ]

    @property
    def msc_enabled(self) -> bool: return self.is_msc_enabled == 1

    @property
    def any_dlc_enabled(self) -> bool: return self.is_msc_enabled == 1 or self.is_watcher_enabled == 1

    @property
    def dlcstate(self) -> str:
        if self.is_msc_enabled:
            if self.is_watcher_enabled:
                return "MSC_Watcher"
            else:
                return "MSC"
        elif self.is_watcher_enabled:
            return "Watcher"
        else:
            return "Vanilla"

    @property
    def starting_scug(self) -> str: return self.which_campaign.scug_id

    @property
    def worldstate(self) -> tuple[str, str]: return self.which_game_version.string, self.dlcstate

    @property
    def which_gamestate_integer(self) -> int:
        return int(self.which_campaign) + (10 if self.is_msc_enabled else 0)

    def find_starting_region(self, random: Random):
        if self.randomize_starting_region == 0:
            return
        elif self.randomize_starting_region == 1:
            choice_counter = Counter({reg: self.possible_starting_regions[reg] for reg in self.possible_starting_regions.keys()
                 if reg in self.possible_starting_regions.names})
        else:
            choice_counter = Counter(self.possible_starting_regions.default)
        valid_codes = {self.possible_starting_regions.names[reg] for reg in choice_counter.keys()}

        def choose_weighted():
            weighted_choices = [reg for reg in choice_counter.elements() if self.possible_starting_regions.names[reg] in valid_codes]
            if not weighted_choices:
                raise OptionError(f"None of the selected regions in \"Possible Starting Regions\" are valid with these options.")
            self.starting_region_name = random.choice(weighted_choices)
            self.starting_region_code = self.possible_starting_regions.names[self.starting_region_name]

        # Filter Watcher regions
        if self.starting_scug == "Watcher":
            valid_codes.intersection_update(story_regions_watcher)
            choose_weighted()
            return
        else:
            valid_codes.difference_update(story_regions_watcher)

        # No Shaded if difficulty_glow
        if self.difficulty_glow:
            valid_codes.difference_update({"SH"})

        # Return vanilla regions if no MSC
        if not self.msc_enabled:
            valid_codes.intersection_update(story_regions_vanilla)
            choose_weighted()
            return

        # Don't spawn in the final region for story endings
        if self.which_victory_condition == "story":
            if self.starting_scug == "Artificer":
                valid_codes.difference_update({"LC"})
            valid_codes.difference_update({"OE"})

        if not self.submerged_should_populate:
            valid_codes.difference_update({"MS"})
        elif self.difficulty_submerged > (1 if self.starting_scug == "Rivulet" else 0):
            valid_codes.difference_update({"MS"})

        # Filter to slugcat's regions
        valid_codes.intersection_update(all_regions["MSC"][self.starting_scug])
        choose_weighted()

    def general_validity_check(self) -> str | None:
        if self.is_watcher_enabled and self.which_game_version < 1100000:
            return "The Watcher cannot be enabled with a game version before 1.10.0."
        if self.is_msc_enabled and self.which_game_version < 1090000:
            return "More Slugcats Expansion cannot be enabled with a game version before 1.9.0."

        if not self.is_watcher_enabled and self.starting_scug == "Watcher":
            return "Watcher's campaign cannot be selected without The Watcher enabled."
        if not self.is_msc_enabled and self.starting_scug in [
            "Gourmand", "Artificer", "Rivulet", "Spear", "Saint", "Inv"]:
            return (f"{self.which_campaign.scug_name}'s campaign cannot be selected "
                    f"without More Slugcats Expansion enabled.")

        if sum(self.get_nontrap_weight_dict().values()) == 0:
            return ("At least one non-trap filler weight must be nonzero."
                    "To disable non-trap filler, set `pct_traps` to 100.")
        if sum(self.get_trap_weight_dict().values()) == 0:
            return ("At least one trap filler weight must be nonzero."
                    "To disable traps, set `pct_traps` to 0.")

        optional_check_score = (
            (2 if self.checks_sheltersanity else 0)
            + (1 if self.checks_flowersanity else 0)
            + (1 if self.checks_devtokens and self.msc_enabled else 0)
            + (1 if self.checks_foodquest and self.msc_enabled else 0)
        )

        if optional_check_score < 2:
            start = self.starting_region_code
            sphere_1_too_small = False
            solutions = [
                "Pick a different starting region.",
                "Enable sheltersanity.",
                "Enable MSC and at least two of flowersanity, devtokens, and foodquest."
            ]

            if (start == "SS" and self.starting_scug != "Rivulet") or start == "UW":
                sphere_1_too_small = True
            elif start == "SB" and self.difficulty_glow:
                sphere_1_too_small = True
                solutions.append("Disable `difficulty_glow`.")
            elif start == "SI" and not self.msc_enabled and self.starting_scug == "Yellow":
                sphere_1_too_small = True
                solutions[2] = "Enable MSC."

            if sphere_1_too_small:
                solution_string = "\n".join(f"{i+1}) {s}" for i, s in enumerate(solutions))
                return ("Sphere 1 is too small with these settings.  "
                        f"Do at least one of the following: \n{solution_string}")

        if self.which_victory_condition == 1 and self.starting_scug == "Rivulet" and not self.submerged_should_populate:
            return f"Rivulet's story ending requires checks in Submerged Superstructure to be enabled."

        if self.which_victory_condition == 3:
            if not self.msc_enabled:
                return (f"Food quest victory condition cannot be selected "
                        f"without More Slugcats Expansion enabled.")
            if (self.starting_scug == "Gourmand") + self.checks_foodquest.value < 2:
                return "Food quest checks must be enabled to use food quest victory condition."

        if self.starting_scug != "Watcher" and (self.which_victory_condition == 4 or self.which_victory_condition == 5):
            return "Victory conditions 'Weaver' and 'True Ending' are not valid for any slugcat other than Watcher."

        if self.which_victory_condition == 2 and self.starting_scug == "Watcher":
            return f"Watcher cannot currently use Echoes victory condition."

        return None

    @property
    def data_block(self) -> dict: return static_data[self.which_game_version.string][self.dlcstate]

    @property
    def submerged_should_populate(self) -> bool:
        return self.checks_submerged + (self.starting_scug == "Rivulet" or "Aquatic Perk" in self.expedition_perks.value) > 1

    def get_nontrap_weight_dict(self) -> dict[str, float]:
        ret = {a.item_name: a.value for a in [
            self.wt_rocks, self.wt_spears, self.wt_explosive_spears, self.wt_grenades,
            self.wt_flashbangs, self.wt_sporepuffs, self.wt_cherrybombs, self.wt_bubble_weed,
            self.wt_lilypucks, self.wt_dandelion_peaches, self.wt_gooieducks, self.wt_fruit, self.wt_bubblefruit,
            self.wt_eggbugeggs, self.wt_jellyfish, self.wt_mushrooms, self.wt_slimemold,
            self.wt_fireeggs, self.wt_glowweed, self.wt_electric_spears, self.wt_singularity_bombs,
            self.wt_lanterns, self.wt_karma_flowers, self.wt_vulture_masks, self.wt_pearls, self.wt_beehives,
            self.wt_joke_rifles, self.wt_boomerangs, self.wt_poison_spears, self.wt_graffiti_bombs, self.wt_rot_fruit,
            self.wt_fire_sprite_larva,
        ]}
        if not self.msc_enabled:
            for key in ("Fire Egg", "Electric Spear", "Joke Rifle"):
                ret[f"{key}"] = 0
        if not self.is_watcher_enabled:
            for key in ("Boomerang", "Poison Spear", "Graffiti Bomb", "Rot Fruit", "Fire Sprite Larva"):
                ret[f"{key}"] = 0
        if not self.any_dlc_enabled:
            for key in ("Lilypuck", "Dandelion Peach", "Glow Weed", "Singularity Bomb", "Gooieduck"):
                ret[f"{key}"] = 0

        return ret

    def get_trap_weight_dict(self) -> dict[str, float]:
        ret = {a.item_name: a.value for a in [
            self.wt_stuns, self.wt_zoomies, self.wt_timers, self.wt_alarms, self.wt_killsquads,
            self.wt_gravity, self.wt_rains, self.wt_fogs,

            self.wt_redcentipede, self.wt_redlizard, self.wt_spitterspider,
            self.wt_brotherlonglegs, self.wt_daddylonglegs, self.wt_responsibility,
            self.wt_ripplespawn, self.wt_blizzardlizard,
        ]}
        if not self.msc_enabled:
            ret["Responsibility"] = 0
        if not self.is_watcher_enabled:
            for key in ("Ripple Spawn", "BlizzardLizard"):
                ret[f"{key}"] = 0

        return ret

    def satisfies(self, flag: GameStateFlag): return flag[self.dlcstate, self.starting_scug]

    def satisfies_flagmap(self, d: ScugFlagMap) -> bool:
        return self.starting_scug in d.get(self.which_game_version.string, self.dlcstate)

    @property
    def should_have_rot_spread_checks(self):
        return (self.starting_scug == "Watcher" and not self.will_be_weaving and
                (self.checks_spread_rot + (self.which_victory_condition == "story")) > 1)

    @property
    def will_be_weaving(self):
        """Whether the player will need to seal portals during this run (Watcher with Weaver or True Ending goal)"""
        return self.starting_scug == "Watcher" and (self.which_victory_condition == 4 or self.which_victory_condition == 5)


option_groups = [
    OptionGroup("Important", RainWorldOptions.group_important),
    OptionGroup("Difficulty settings", RainWorldOptions.group_difficulty, True),
    OptionGroup("Check pool settings", RainWorldOptions.group_checkpool, True),
    OptionGroup("Item pool settings", RainWorldOptions.group_itempool, True),
    OptionGroup("Watcher-specific settings", RainWorldOptions.group_watcher, True),
    OptionGroup("Filler item relative weights", RainWorldOptions.group_filler, True),
    OptionGroup("Trap relative weights", RainWorldOptions.group_traps, True),
]
