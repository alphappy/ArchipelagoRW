from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle, Range, OptionGroup, Choice, ProgressionBalancing, Accessibility, \
    Visibility, DeathLinkMixin, DeathLink
from .conditions import GameStateFlag


#################################################################
# IMPORTANT SETTINGS
class PassageProgressWithoutSurvivor(Toggle):
    """Whether The Dragon Slayer, The Friend, and The Wanderer are completable without completing The Survivor.
    This will override the actual value of the corresponding setting in the Rain World Remix menu."""
    display_name = "Passage progress without Survivor"
    default = True


class WhichGamestate(Choice):
    """Which campaign and worldstate you will start in.
    If an MSC state is selected, MSC **must** be enabled in-game."""
    display_name = "Game state"
    option_monk_vanilla = 0
    option_survivor_vanilla = 1
    option_hunter_vanilla = 2

    option_monk_msc = 10
    option_survivor_msc = 11
    option_hunter_msc = 12
    option_gourmand = 13
    option_artificer = 14
    option_rivulet = 15
    option_spearmaster = 16
    option_saint = 17
    option_sofanthiel = 18

    default = 1

    ids_names = {
        0: ("Yellow", "Monk"),
        1: ("White", "Survivor"),
        2: ("Red", "Hunter"),
        10: ("Yellow", "Monk"),
        11: ("White", "Survivor"),
        12: ("Red", "Hunter"),
        13: ("Gourmand", "Gourmand"),
        14: ("Artificer", "Artificer"),
        15: ("Rivulet", "Rivulet"),
        16: ("Spear", "Spearmaster"),
        17: ("Saint", "Saint"),
        18: ("Inv", "Sofanthiel"),
    }

    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value < 19:
            return f"{cls.ids_names[value][1]}{' (Vanilla)' if value < 10 else (' (MSC)' if value < 13 else '')}"
        return f"{value}"

    @property
    def scug_id(self) -> str:
        return self.__class__.ids_names[self.value][0]

    @property
    def scug_name(self) -> str:
        return self.__class__.ids_names[self.value][1]

    @property
    def dlcstate(self) -> str:
        return "MSC" if self.value > 9 else "Vanilla"


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


class ChecksTokensPearls(Toggle):
    """Whether all tokens and pearls should be visible to all slugcats."""
    display_name = "All tokens and pearls"
    default = False
    visibility = Visibility.none


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


class DifficultyExtremeThreats(Choice):
    """Whether eliminating an extreme threat could be required.
    This includes Red Lizards for The Dragon Slayer and Red Centipedes or Aquapedes for the food quest.
    "Capable slugcats" include Gourmand, Artificer, Spearmaster and Sofanthiel."""
    display_name = "Extreme threats"
    option_all_slugcats = 2
    option_capable_slugcats = 1
    option_off = 0
    default = 1


class DifficultySubmerged(Toggle):
    """Whether Submerged Superstructure is logically locked behind advancing the story state for Rivulet.
    Advancing the story state - normally done by removing the rarefaction cell from The Rot -
    causes the cycle duration to increase significantly, making Submerged Superstructure significantly easier.

    This setting only impacts Rivulet."""
    display_name = "Late Submerged"
    default = True


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
    item_name = "Object-Rock"
    default = 100


class WtSpear(WtGeneric):
    """The relative weight of spears in the non-trap filler item pool."""
    display_name = "Spear"
    item_name = "Object-Spear"
    default = 40


class WtExplosiveSpear(WtGeneric):
    """The relative weight of explosive spears in the non-trap filler item pool."""
    display_name = "ExplosiveSpear"
    item_name = "Object-ExplosiveSpear"
    default = 10


class WtGrenade(WtGeneric):
    """The relative weight of grenades in the non-trap filler item pool."""
    display_name = "Grenade"
    item_name = "Object-ScavengerBomb"
    default = 10


class WtFlashbang(WtGeneric):
    """The relative weight of flashbangs in the non-trap filler item pool."""
    display_name = "Flashbang"
    item_name = "Object-FlareBomb"
    default = 20


class WtSporePuff(WtGeneric):
    """The relative weight of spore puffs in the non-trap filler item pool."""
    display_name = "Spore puff"
    item_name = "Object-PuffBall"
    default = 20


class WtCherrybomb(WtGeneric):
    """The relative weight of cherrybombs in the non-trap filler item pool."""
    display_name = "Cherrybomb"
    item_name = "Object-FirecrackerPlant"
    default = 30


class WtLillyPuck(WtGeneric):
    """The relative weight of lilypucks in the non-trap filler item pool."""
    display_name = "Lilypuck (MSC)"
    item_name = "Object-LillyPuck"
    default = 20


class WtFruit(WtGeneric):
    """The relative weight of blue fruit in the non-trap filler item pool."""
    display_name = "Blue fruit"
    item_name = "Object-DangleFruit"
    default = 60


class WtBubbleFruit(WtGeneric):
    """The relative weight of bubble fruit in the non-trap filler item pool."""
    display_name = "Bubble fruit"
    item_name = "Object-WaterNut"
    default = 40


class WtEggbugEgg(WtGeneric):
    """The relative weight of eggbug eggs in the non-trap filler item pool."""
    display_name = "Eggbug egg"
    item_name = "Object-EggBugEgg"
    default = 30


class WtJellyfish(WtGeneric):
    """The relative weight of jellyfish in the non-trap filler item pool."""
    display_name = "Jellyfish"
    item_name = "Object-JellyFish"
    default = 15


class WtMushroom(WtGeneric):
    """The relative weight of mushrooms in the non-trap filler item pool."""
    display_name = "Mushroom"
    item_name = "Object-Mushroom"
    default = 15


class WtSlimeMold(WtGeneric):
    """The relative weight of slime mold in the non-trap filler item pool."""
    display_name = "Slime mold"
    item_name = "Object-SlimeMold"
    default = 35


class WtFireEgg(WtGeneric):
    """The relative weight of firebug eggs in the non-trap filler item pool."""
    display_name = "Firebug egg (MSC)"
    item_name = "Object-FireEgg"
    default = 5


class WtGlowWeed(WtGeneric):
    """The relative weight of glow weed in the non-trap filler item pool."""
    display_name = "Glow weed (MSC)"
    item_name = "Object-GlowWeed"
    default = 15


class WtElectricSpear(WtGeneric):
    """The relative weight of electric spears in the non-trap filler item pool."""
    display_name = "Electric spear (MSC)"
    item_name = "Object-ElectricSpear"
    default = 3


class WtSingularityBomb(WtGeneric):
    """The relative weight of singularity bombs in the non-trap filler item pool."""
    display_name = "Singularity Bomb (MSC)"
    item_name = "Object-SingularityBomb"
    default = 1


class WtLantern(WtGeneric):
    """The relative weight of lanterns in the non-trap filler item pool."""
    display_name = "Lantern"
    item_name = "Object-Lantern"
    default = 15


class WtKarmaFlower(WtGeneric):
    """The relative weight of karma flowers in the non-trap filler item pool."""
    display_name = "Karma flower"
    item_name = "Object-KarmaFlower"
    default = 5


class WtVultureMask(WtGeneric):
    """The relative weight of vulture masks in the non-trap filler item pool."""
    display_name = "Vulture mask"
    item_name = "Object-VultureMask"
    default = 9


class WtJokeRifle(WtGeneric):
    """The relative weight of joke rifles in the non-trap filler item pool."""
    display_name = "Joke rifle (MSC)"
    item_name = "Object-JokeRifle"
    default = 1


#################################################################
# TRAP SETTINGS
class WtTrapStun(WtGeneric):
    """The relative weight of stun traps in the trap filler item pool."""
    display_name = "Stun"
    item_name = "Trap-Stun"
    default = 100


class WtTrapZoomies(WtGeneric):
    """The relative weight of zoomies traps in the trap filler item pool."""
    display_name = "Zoomies"
    item_name = "Trap-Zoomies"
    default = 70


class WtTrapTimer(WtGeneric):
    """The relative weight of timer traps in the trap filler item pool."""
    display_name = "Timer"
    item_name = "Trap-Timer"
    default = 100


class WtTrapRedLizard(WtGeneric):
    """The relative weight of red lizard traps in the trap filler item pool."""
    display_name = "RedLizard"
    item_name = "Trap-RedLizard"
    default = 40


class WtTrapRedCentipede(WtGeneric):
    """The relative weight of red centipede traps in the trap filler item pool."""
    display_name = "RedCentipede"
    item_name = "Trap-RedCentipede"
    default = 25


class WtTrapSpitterSpider(WtGeneric):
    """The relative weight of spitter spider traps in the trap filler item pool."""
    display_name = "RedCentipede"
    item_name = "Trap-RedCentipede"
    default = 30


class WtTrapBrotherLongLegs(WtGeneric):
    """The relative weight of brother long legs traps in the trap filler item pool."""
    display_name = "BrotherLongLegs"
    item_name = "Trap-BrotherLongLegs"
    default = 15


class WtTrapDaddyLongLegs(WtGeneric):
    """The relative weight of daddy long legs traps in the trap filler item pool."""
    display_name = "DaddyLongLegs"
    item_name = "Trap-DaddyLongLegs"
    default = 5


class WtTrapFlood(WtGeneric):
    """The relative weight of flood traps in the trap filler item pool."""
    display_name = "Flood"
    item_name = "Trap-Flood"
    default = 0
    visibility = Visibility.none


class WtTrapRain(WtGeneric):
    """The relative weight of rain traps in the trap filler item pool."""
    display_name = "Rain"
    item_name = "Trap-Rain"
    default = 0
    visibility = Visibility.none


class WtTrapGravity(WtGeneric):
    """The relative *weight* of gravity traps in the trap filler item pool."""
    display_name = "Gravity"
    item_name = "Trap-Gravity"
    default = 0
    visibility = Visibility.none


class WtTrapFog(WtGeneric):
    """The relative weight of fog traps in the trap filler item pool."""
    display_name = "Fog"
    item_name = "Trap-Fog"
    default = 0
    visibility = Visibility.none


class WtTrapKillSquad(WtGeneric):
    """The relative weight of kill squad traps in the trap filler item pool."""
    display_name = "KillSquad"
    item_name = "Trap-KillSquad"
    default = 0
    visibility = Visibility.none


class WtTrapAlarm(WtGeneric):
    """The relative weight of alarm traps in the trap filler item pool."""
    display_name = "Alarm"
    item_name = "Trap-Alarm"
    default = 15


@dataclass
class RainWorldOptions(PerGameCommonOptions, DeathLinkMixin):
    #################################################################
    # IMPORTANT SETTINGS
    passage_progress_without_survivor: PassageProgressWithoutSurvivor
    which_gamestate: WhichGamestate
    which_victory_condition: WhichVictoryCondition
    which_gate_behavior: WhichGateBehavior
    random_starting_region: RandomStartingRegion

    group_important = [
        PassageProgressWithoutSurvivor, WhichGamestate, WhichVictoryCondition, WhichGateBehavior, DeathLink,
        RandomStartingRegion
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

    group_difficulty = [
        ProgressionBalancing, Accessibility, DifficultyMonk, DifficultyHunter, DifficultyOutlaw, DifficultyNomad,
        DifficultyChieftain, DifficultyGlow, DifficultyExtremeThreats, DifficultySubmerged
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
    passage_priority: PassagePriority
    checks_tokens_pearls: ChecksTokensPearls

    group_checkpool = [
        ChecksBroadcasts, ChecksFoodQuest, PassagePriority, ChecksTokensPearls
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
    def msc_enabled(self) -> bool: return self.which_gamestate.value > 9

    @property
    def dlcstate(self) -> str: return self.which_gamestate.dlcstate

    @property
    def starting_scug(self) -> str: return self.which_gamestate.scug_id

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
            for key in ("LillyPuck", "FireEgg", "GlowWeed", "ElectricSpear", "SingulaityBomb", "JokeRifle"):
                ret[f"Object-{key}"] = 0

        return ret

    def get_trap_weight_dict(self) -> dict[str, float]:
        return {a.item_name: a.value for a in [
            self.wt_stuns, self.wt_zoomies, self.wt_timers, self.wt_alarms, self.wt_killsquads,
            self.wt_gravity, self.wt_rains, self.wt_floods, self.wt_fogs,

            self.wt_redcentipede, self.wt_redlizard, self.wt_spitterspider,
            self.wt_brotherlonglegs, self.wt_daddylonglegs
        ]}

    def satisfies(self, flag: GameStateFlag): return flag[self.dlcstate, self.starting_scug]


option_groups = [
    OptionGroup("Important", RainWorldOptions.group_important),
    OptionGroup("Difficulty settings", RainWorldOptions.group_difficulty, True),
    OptionGroup("Check pool settings", RainWorldOptions.group_checkpool, True),
    OptionGroup("Item pool settings", RainWorldOptions.group_itempool, True),
    OptionGroup("Filler item relative weights", RainWorldOptions.group_filler, True),
    OptionGroup("Trap relative weights", RainWorldOptions.group_traps, True),
]
