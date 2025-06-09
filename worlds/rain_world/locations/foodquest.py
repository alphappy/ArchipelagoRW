from BaseClasses import MultiWorld
from .classes import LocationData, AbstractLocation
from ..conditions.classes import Simple
from ..game_data.general import extreme_threat_creatures, wiki_names
from ..game_data.bitflag import ScugFlag
from ..options import RainWorldOptions

_offset = 5250


class FoodQuestPip(AbstractLocation):
    def __init__(self, gamestates: int, items: str | list[str], proper_name: str | None = None):
        global _offset
        self.items = [items] if type(items) == str else items
        names = self.names(self.items)
        if proper_name is not None:
            names.insert(0, f"Food Quest - {proper_name}")
        super().__init__(names[0], names[-1], names[1:-1], _offset, "Food Quest")
        _offset += 1
        self.scugflag = ScugFlag(gamestates)
        self.expanded = False
        self.access_condition = Simple(items, 1)

    @staticmethod
    def names(items: list[str]) -> list[str]:
        ret = []
        re_items = set(items).difference({"DeadHazer", "DeadVultureGrub"})
        for itemlist in [[wiki_names[item][0] for item in re_items], re_items]:
            ret += [f"Food Quest - {' or '.join(itemlist)}"]
            if len(itemlist) > 0:
                ret += [f"Food Quest - {item}" for item in itemlist]
        ret += [f"FoodQuest-{items[0]}"]
        return ret

    def pre_generate(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        if options.starting_scug not in self.scugflag:
            return False
        if self.items[0] in extreme_threat_creatures and not options.difficulty_extreme_threats:
            return False
        if self.expanded and not options.checks_foodquest_expanded:
            return False
        # HARDCODE: Sofanthiel's only glow weed is in MS.  The interactive map is wrong.
        if options.starting_scug == "Inv" and options.checks_submerged < 2 and self.items[0] == "GlowWeed":
            return False
        return super().pre_generate(player, multiworld, options)


pips: list[FoodQuestPip] = [
    FoodQuestPip(0b1_110_111_111, "SlimeMold"),
    FoodQuestPip(0b1_110_111_111, "DangleFruit"),
    FoodQuestPip(0b1_101_111_111, "Fly"),
    FoodQuestPip(0b1_111_111_111, "Mushroom"),
    FoodQuestPip(0b0_101_011_100, "BlackLizard"),
    FoodQuestPip(0b1_110_111_111, "WaterNut"),
    FoodQuestPip(0b1_100_111_111, "JellyFish"),
    FoodQuestPip(0b0_101_011_100, "JetFish"),
    # Artificer can eat glow weed, but there are none in that gamestate.
    FoodQuestPip(0b1_110_101_111, "GlowWeed"),
    FoodQuestPip(0b0_101_011_100, ["Salamander", "EelLizard"]),
    FoodQuestPip(0b0_101_011_100, "Snail"),
    FoodQuestPip(0b1_101_111_111, ["Hazer", "DeadHazer"]),
    FoodQuestPip(0b0_101_011_100, "EggBug"),
    FoodQuestPip(0b1_110_111_111, "LillyPuck"),
    FoodQuestPip(0b0_101_011_100, "YellowLizard"),
    FoodQuestPip(0b0_101_011_100, "TubeWorm"),
    FoodQuestPip(0b0_111_111_111, "SSOracleSwarmer"),
    FoodQuestPip(0b0_101_111_111, "Centiwing"),
    FoodQuestPip(0b1_110_111_111, "DandelionPeach"),
    FoodQuestPip(0b0_101_011_100, "CyanLizard"),
    FoodQuestPip(0b1_110_111_111, "GooieDuck"),
    FoodQuestPip(0b1_101_111_111, ["RedCentipede", "AquaCenti"]),

    FoodQuestPip(0b1_111_111_111, "SeedCob"),
    FoodQuestPip(0b1_101_111_111, ["Centipede", "SmallCentipede"], "Centipede"),
    FoodQuestPip(0b1_101_111_111, ["VultureGrub", "DeadVultureGrub"]),
    FoodQuestPip(0b1_101_111_111, ["SmallNeedleWorm", "BigNeedleWorm"], "Noodlefly"),
    FoodQuestPip(0b0_101_011_100, "GreenLizard"),
    FoodQuestPip(0b0_101_011_100, "BlueLizard"),
    FoodQuestPip(0b0_101_011_100, "PinkLizard"),
    FoodQuestPip(0b0_101_011_100, "WhiteLizard"),
    FoodQuestPip(0b0_101_011_100, "RedLizard"),
    FoodQuestPip(0b0_101_011_100, "SpitLizard"),
    FoodQuestPip(0b0_100_000_000, "ZoopLizard"),
    FoodQuestPip(0b0_100_000_000, "TrainLizard"),
    FoodQuestPip(0b0_101_011_100, "BigSpider"),
    FoodQuestPip(0b0_101_011_100, "SpitterSpider"),
    FoodQuestPip(0b0_101_011_100, "MotherSpider"),
    # All vultures are Miros for Sofanthiel.  There are no Miros for Hunter/Gourmand.
    FoodQuestPip(0b0_001_011_100, "Vulture"),
    FoodQuestPip(0b0_001_011_100, "KingVulture"),
    FoodQuestPip(0b0_101_010_000, "MirosVulture"),
    FoodQuestPip(0b0_101_011_100, "LanternMouse"),
    FoodQuestPip(0b0_101_011_100, ["CicadaA", "CicadaB"], "Squidcada"),
    FoodQuestPip(0b0_100_001_000, "Yeek"),
    FoodQuestPip(0b0_101_011_100, "DropBug"),
    FoodQuestPip(0b0_101_011_100, "MirosBird"),
    FoodQuestPip(0b0_101_011_100, ["Scavenger", "ScavengerElite"], "Scavenger"),
    FoodQuestPip(0b0_101_011_100, ["DaddyLongLegs", "BrotherLongLegs", "TerrorLongLegs", "HunterDaddy"], "Rot"),
    FoodQuestPip(0b0_001_000_000, "PoleMimic"),
    FoodQuestPip(0b0_001_000_000, "TentaclePlant"),
    FoodQuestPip(0b0_001_000_000, "BigEel"),
    FoodQuestPip(0b0_001_000_000, "Inspector"),
]

for i in range(22, len(pips)):
    pips[i].expanded = True


def generate(options: RainWorldOptions) -> list[LocationData]:
    if options.msc_enabled and (options.starting_scug == "Gourmand") + options.checks_foodquest.value > 1:
        return pips
    return []
