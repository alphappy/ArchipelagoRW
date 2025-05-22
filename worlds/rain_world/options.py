from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle, Range, OptionGroup, Choice, ProgressionBalancing, Accessibility, \
    Visibility, DeathLinkMixin, DeathLink
from .conditions import GameStateFlag
from .game_data import static_data


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
    option_1_10_1 = 1100100
    alias_1_10 = 1100100
    default = 1100100

    displaying = {
        1091503: ("v1.9.15b / v1.9.15.3", "1.9.15.3"),
        1100100: ("v1.10.0 - v1.10.1", "1.10.1"),
    }

    @property
    def string(self) -> str: return self.displaying[self.value][1]

    @classmethod
    def get_option_name(cls, value: int) -> str: return cls.displaying[value][0]


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
    """Whether ascension or a gamestate-specific alternative is the victory condition.
    The alternative victory condition depends on the selected gamestate.

    **Vanilla**, **Hunter**, **Saint**, or **Sofanthiel**: No alternate.

    **Monk** and **Survivor**: Reach Journey's End in Outer Expanse.

    **Gourmand**: Receive the Mark and reach Journey's End in Outer Expanse.

    **Artificer**: Receive the Mark and kill the Chieftain in Metropolis.

    **Rivulet**: Receive the Rarefaction Cell and deliver it to Submerged Superstructure,
    then meet Looks to the Moon.

    **Spearmaster**: Receive the Mark, the SM pearl, and Moon's message,
    then deliver it to Communications Array in Sky Islands.
    """
    display_name = "Victory condition"
    option_ascension = 0
    option_alternate = 1


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


#################################################################
# WATCHER SETTINGS
class RippleWarpBehavior(Choice):
    """How ripple warps behave.  See the settings documentation for explanation."""
    display_name = "Ripple warp behavior"
    option_unaltered = 0
    option_no_ripple_warps = 1
    default = 0


class NormalDynamicWarpBehavior(Choice):
    """How normal dynamic warps behave.  See the Watcher documentation for explanation."""
    display_name = "Normal dynamic warp behavior"
    option_ignored = 0
    option_visited = 1
    option_static_pool = 2
    option_unlockable_pool = 4
    option_predetermined = 5
    default = 1


class ThroneDynamicWarpBehavior(Choice):
    """How Throne dynamic warps behave.  See the Watcher documentation for explanation."""
    display_name = "Throne dynamic warp behavior"
    option_ignored = 0
    option_visited = 1
    option_predetermined = 5
    default = 5


class DynamicWarpPoolSize(Range):
    """Number of regions in the dynamic warp pool.  See the Watcher documentation for explanation."""
    display_name = "Normal pool size"
    range_start = 1
    range_end = 18
    default = 18


class LogicRottedGeneration(Choice):
    """Controls the generation of Crumbling Fringes, Corrupted Factories, Decaying Tunnels, and Infested Wastes."""
    display_name = "Permarotted accessibility"
    option_none = 0
    option_passthrough = 2
    option_full = 3
    default = 0


class LogicMinRippleTarget(Range):
    """The lowest that your *minimum* Ripple can be before Ripplespace is logically accessible.
    The default, 5, matches the actual game behavior."""
    display_name = "Min Ripple target"
    range_start = 5
    range_end = 9
    default = 5


class RottedRegionTarget(Range):
    """The number of regions that must be rotted for the Rot ending.
    The default, 18, matches the unaltered game behavior."""
    display_name = "Rotted region target"
    range_start = 2
    range_end = 18
    default = 18


class ChecksSpreadRot(Choice):
    """Whether spreading the Rot to a new region is a check."""
    option_off = 0
    option_alternate_only = 1
    option_on = 2
    default = 1


#################################################################
# GENERAL SETTINGS
class RandomStartingRegion(Choice):
    """Where Slugcat will initially spawn.
    If not set to default, a random shelter in the region is selected."""
    display_name = "Random starting shelter"
    option_default_starting_point = 0

    option_outskirts = 1
    option_industrial_complex = 2
    option_drainage_system = 3
    option_garbage_wastes = 4
    option_shoreline = 5
    option_shaded_citadel = 6
    option_the_exterior = 7
    option_five_pebbles = 8
    option_chimney_canopy = 9
    option_sky_islands = 10
    option_farm_arrays = 11
    option_subterranean = 12
    option_pipeyard = 20
    option_outer_expanse = 22
    option_metropolis = 23
    option_looks_to_the_moon = 24

    option_sunlit_port = 30

    alias_undergrowth = 3
    alias_waterfront_facility = 5
    alias_silent_construct = 6
    alias_the_rot = 8

    default = 0

    names = {
        0: ("Default starting point", "!!!"),
        1: ("Outskirts", "SU"),
        2: ("Industrial Complex", "HI"),
        3: ("Drainage System / Undergrowth", "DS"),
        4: ("Garbage Wastes", "GW"),
        5: ("Shoreline / Waterfront Facility", "SL"),
        6: ("Shaded Citadel / Silent Construct", "SH"),
        7: ("The Exterior", "UW"),
        8: ("Five Pebbles / The Rot", "SS"),
        9: ("Chimney Canopy", "CC"),
        10: ("Sky Islands", "SI"),
        11: ("Farm Arrays", "LF"),
        12: ("Subterranean", "SB"),
        20: ("Pipeyard", "VS"),
        22: ("Outer Expanse", "OE"),
        23: ("Metropolis", "LC"),
        24: ("Looks to the Moon", "DM"),

        30: ("Sunlit Port", "WSKB"),
    }

    @classmethod
    def get_option_name(cls, value: int) -> str:
        return cls.names[value][0]

    @property
    def code(self) -> str:
        return self.__class__.names[self.value][1]

    @property
    def name(self) -> str:
        return self.__class__.names[self.value][0]


class PassagePriority(Range):
    """Number of Passages that are randomly marked as priority checks,
    increasing the chance that they will contain progression items.
    These are in addition to any manually-prioiritized Passages,
    and will not override any manually-excluded Passages."""
    display_name = "Priority Passages"
    range_start = 0
    range_end = 14
    default = 5


class ExtraKarmaCapIncreases(Range):
    """Number of extra karma cap increases in the pool beyond the minimum required for ascension."""
    display_name = "Extra karma cap increases"
    range_start = 0
    range_end = 30
    default = 1


#################################################################
# CHECK POOL SETTINGS
class ChecksBroadcasts(Choice):
    """Which slugcats broadcasts should be available to.  Requires MSC."""
    display_name = "Broadcasts"
    option_all_slugcats = 2
    option_only_spearmaster = 1
    option_off = 0
    default = 1
    visibility = Visibility.none


class ChecksFoodQuest(Choice):
    """Which slugcats the food quest should be available to.  Requires MSC."""
    display_name = "Food quest"
    option_all_slugcats = 2
    option_only_gourmand = 1
    option_off = 0
    default = 2


class ChecksFoodQuestExpanded(Toggle):
    """Whether the food quest should be expanded to include most creatures.
    Specific food quest checks may be disabled by excluding the locations,
    and some slugcats will not be required to kill and eat extreme threats if that setting is enabled.
    Requires MSC."""
    display_name = "Expanded food quest"
    default = True


class ChecksTokensPearls(Toggle):
    """Whether all tokens and pearls should be visible to all slugcats."""
    display_name = "All tokens and pearls"
    default = False
    visibility = Visibility.none


class ChecksSheltersanity(Toggle):
    """Whether each shelter is a check."""
    display_name = "Sheltersanity"
    default = False


class ChecksSubmerged(Choice):
    """Whether Submerged Superstructure has any checks."""
    display_name = "Include Submerged"
    option_all_slugcats = 2
    option_only_rivulet = 1
    option_off = 0
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


class DifficultySubmerged(Toggle):
    """Whether Submerged Superstructure is logically locked behind advancing the story state for Rivulet.
    Advancing the story state - normally done by removing the rarefaction cell from The Rot -
    causes the cycle duration to increase significantly, making Submerged Superstructure significantly easier.

    This setting only impacts Rivulet."""
    display_name = "Late Submerged"
    default = True


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
# FILLER SETTINGS
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


class WtLillyPuck(WtGeneric):
    """The relative weight of lilypucks in the non-trap filler item pool."""
    display_name = "Lilypuck (MSC)"
    item_name = "Lilypuck"
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


class WtJokeRifle(WtGeneric):
    """The relative weight of joke rifles in the non-trap filler item pool."""
    display_name = "Joke Rifle (MSC)"
    item_name = "Joke Rifle"
    default = 1


#################################################################
# TRAP SETTINGS
class WtTrapStun(WtGeneric):
    """The relative weight of stun traps in the trap filler item pool."""
    display_name = "Stun trap"
    item_name = "Stun trap"
    default = 100


class WtTrapZoomies(WtGeneric):
    """The relative weight of zoomies traps in the trap filler item pool."""
    display_name = "Zoomies trap"
    item_name = "Zoomies trap"
    default = 70


class WtTrapTimer(WtGeneric):
    """The relative weight of timer traps in the trap filler item pool."""
    display_name = "Timer trap"
    item_name = "Timer trap"
    default = 100


class WtTrapRedLizard(WtGeneric):
    """The relative weight of red lizard traps in the trap filler item pool."""
    display_name = "Red Lizard trap"
    item_name = "Red Lizard trap"
    default = 40


class WtTrapRedCentipede(WtGeneric):
    """The relative weight of red centipede traps in the trap filler item pool."""
    display_name = "Red Centipede trap"
    item_name = "Red Centipede trap"
    default = 25


class WtTrapSpitterSpider(WtGeneric):
    """The relative weight of spitter spider traps in the trap filler item pool."""
    display_name = "Red Centipede trap"
    item_name = "Red Centipede trap"
    default = 30


class WtTrapBrotherLongLegs(WtGeneric):
    """The relative weight of brother long legs traps in the trap filler item pool."""
    display_name = "Brother Long Legs trap"
    item_name = "Brother Long Legs trap"
    default = 15


class WtTrapDaddyLongLegs(WtGeneric):
    """The relative weight of daddy long legs traps in the trap filler item pool."""
    display_name = "Daddy Long Legs trap"
    item_name = "Daddy Long Legs trap"
    default = 5


class WtTrapFlood(WtGeneric):
    """The relative weight of flood traps in the trap filler item pool."""
    display_name = "Flood trap"
    item_name = "Flood trap"
    default = 0
    visibility = Visibility.none


class WtTrapRain(WtGeneric):
    """The relative weight of rain traps in the trap filler item pool."""
    display_name = "Rain trap"
    item_name = "Rain trap"
    default = 0
    visibility = Visibility.none


class WtTrapGravity(WtGeneric):
    """The relative *weight* of gravity traps in the trap filler item pool."""
    display_name = "Gravity trap"
    item_name = "Gravity trap"
    default = 0
    visibility = Visibility.none


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
    """The relative weight of alarm traps in the trap filler item pool."""
    display_name = "Alarm trap"
    item_name = "Alarm trap"
    default = 15


@dataclass
class RainWorldOptions(PerGameCommonOptions, DeathLinkMixin):
    #################################################################
    # IMPORTANT SETTINGS
    which_game_version: WhichGameVersion
    is_msc_enabled: IsMSCEnabled
    is_watcher_enabled: IsWatcherEnabled
    which_campaign: WhichCampaign
    passage_progress_without_survivor: PassageProgressWithoutSurvivor
    which_victory_condition: WhichVictoryCondition
    which_gate_behavior: WhichGateBehavior
    random_starting_region: RandomStartingRegion

    group_important = [
        WhichGameVersion, IsMSCEnabled, IsWatcherEnabled, WhichCampaign,
        PassageProgressWithoutSurvivor, WhichVictoryCondition, WhichGateBehavior, DeathLink, RandomStartingRegion
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
    pct_traps: PctTraps
    weight_jitter: FillerJitter
    extra_karma_cap_increases: ExtraKarmaCapIncreases

    group_itempool = [
        ExtraKarmaCapIncreases, PctTraps, FillerJitter
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
    checks_karma_flowers: ChecksKarmaFlowers

    group_checkpool = [
        ChecksBroadcasts, ChecksFoodQuest, ChecksFoodQuestExpanded, PassagePriority, ChecksTokensPearls,
        ChecksSheltersanity, ChecksSubmerged, ChecksKarmaFlowers,
    ]

    #################################################################
    # WATCHER-SPECIFIC SETTINGS
    logic_rotted_generation: LogicRottedGeneration
    logic_ripplespace_min_req: LogicMinRippleTarget
    normal_dynamic_warp_behavior: NormalDynamicWarpBehavior
    throne_dynamic_warp_behavior: ThroneDynamicWarpBehavior
    dynamic_warp_pool_size: DynamicWarpPoolSize
    rotted_region_target: RottedRegionTarget
    checks_spread_rot: ChecksSpreadRot

    group_watcher = [
        LogicRottedGeneration, LogicMinRippleTarget, NormalDynamicWarpBehavior, ThroneDynamicWarpBehavior,
        DynamicWarpPoolSize, RottedRegionTarget, ChecksSpreadRot
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
    wt_lanterns: WtLantern
    wt_vulture_masks: WtVultureMask
    wt_lilypucks: WtLillyPuck
    wt_electric_spears: WtElectricSpear
    wt_singularity_bombs: WtSingularityBomb
    wt_joke_rifles: WtJokeRifle

    wt_fruit: WtFruit
    wt_bubblefruit: WtBubbleFruit
    wt_eggbugeggs: WtEggbugEgg
    wt_jellyfish: WtJellyfish
    wt_mushrooms: WtMushroom
    wt_slimemold: WtSlimeMold
    wt_karma_flowers: WtKarmaFlower
    wt_fireeggs: WtFireEgg
    wt_glowweed: WtGlowWeed

    group_filler = [
        WtRock, WtSpear, WtExplosiveSpear, WtGrenade, WtFlashbang, WtSporePuff, WtCherrybomb, WtLantern, WtVultureMask,
        WtFruit, WtBubbleFruit, WtEggbugEgg, WtJellyfish, WtMushroom, WtSlimeMold, WtKarmaFlower,

        WtLillyPuck, WtElectricSpear, WtSingularityBomb, WtJokeRifle,
        WtFireEgg, WtGlowWeed
    ]

    #################################################################
    # TRAP SETTINGS

    wt_stuns: WtTrapStun
    wt_zoomies: WtTrapZoomies
    wt_timers: WtTrapTimer
    wt_killsquads: WtTrapKillSquad
    wt_alarms: WtTrapAlarm
    wt_fogs: WtTrapFog
    wt_floods: WtTrapFlood
    wt_rains: WtTrapRain
    wt_gravity: WtTrapGravity

    wt_redlizard: WtTrapRedLizard
    wt_redcentipede: WtTrapRedCentipede
    wt_spitterspider: WtTrapSpitterSpider
    wt_brotherlonglegs: WtTrapBrotherLongLegs
    wt_daddylonglegs: WtTrapDaddyLongLegs

    group_traps = [
        WtTrapStun, WtTrapZoomies, WtTrapTimer, WtTrapAlarm, WtTrapKillSquad,
        WtTrapGravity, WtTrapRain, WtTrapFlood, WtTrapFog,

        WtTrapRedLizard, WtTrapRedCentipede, WtTrapSpitterSpider,
        WtTrapBrotherLongLegs, WtTrapDaddyLongLegs
    ]

    @property
    def msc_enabled(self) -> bool: return self.is_msc_enabled == 1

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
    def which_gamestate_integer(self) -> int:
        return int(self.which_campaign) + (10 if self.is_msc_enabled else 0)

    def check_gamestate_validity(self) -> str | None:
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

        return None

    @property
    def data_block(self) -> dict: return static_data[self.which_game_version.string][self.dlcstate]

    @property
    def submerged_should_populate(self) -> bool: return self.checks_submerged + (self.starting_scug == "Rivulet") > 1

    def get_nontrap_weight_dict(self) -> dict[str, float]:
        ret = {a.item_name: a.value for a in [
            self.wt_rocks, self.wt_spears, self.wt_explosive_spears, self.wt_grenades,
            self.wt_flashbangs, self.wt_sporepuffs, self.wt_cherrybombs, self.wt_lilypucks,
            self.wt_fruit, self.wt_bubblefruit, self.wt_eggbugeggs, self.wt_jellyfish,
            self.wt_mushrooms, self.wt_slimemold, self.wt_fireeggs, self.wt_glowweed,
            self.wt_electric_spears, self.wt_singularity_bombs, self.wt_lanterns,
            self.wt_karma_flowers, self.wt_vulture_masks, self.wt_joke_rifles,
        ]}
        if not self.msc_enabled:
            for key in ("Lilypuck", "Fire Egg", "Glow Weed", "Electric Spear", "Singularity Bomb", "Joke Rifle"):
                ret[f"{key}"] = 0

        return ret

    def get_trap_weight_dict(self) -> dict[str, float]:
        return {a.item_name: a.value for a in [
            self.wt_stuns, self.wt_zoomies, self.wt_timers, self.wt_alarms, self.wt_killsquads,
            self.wt_gravity, self.wt_rains, self.wt_floods, self.wt_fogs,

            self.wt_redcentipede, self.wt_redlizard, self.wt_spitterspider,
            self.wt_brotherlonglegs, self.wt_daddylonglegs
        ]}

    def satisfies(self, flag: GameStateFlag): return flag[self.dlcstate, self.starting_scug]

    @property
    def should_have_rot_spread_checks(self):
        return (self.starting_scug == "Watcher" and
                (self.checks_spread_rot + (self.which_victory_condition == "alternate")) > 1)


option_groups = [
    OptionGroup("Important", RainWorldOptions.group_important),
    OptionGroup("Difficulty settings", RainWorldOptions.group_difficulty, True),
    OptionGroup("Check pool settings", RainWorldOptions.group_checkpool, True),
    OptionGroup("Item pool settings", RainWorldOptions.group_itempool, True),
    OptionGroup("Watcher-specific settings (spoilers)", RainWorldOptions.group_watcher, True),
    OptionGroup("Filler item relative weights", RainWorldOptions.group_filler, True),
    OptionGroup("Trap relative weights", RainWorldOptions.group_traps, True),
]
