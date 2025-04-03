from BaseClasses import MultiWorld
from .classes import LocationData, AbstractLocation
from ..conditions import GameStateFlag
from ..conditions.classes import Simple
from ..game_data.general import extreme_threat_creatures, wiki_names
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
        self.gamestates = GameStateFlag(gamestates)
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
        if not options.satisfies(self.gamestates):
            return False
        if self.items[0] in extreme_threat_creatures and options.difficulty_extreme_threats + (options.starting_scug not in ["Gourmand", "Artificer", "Spear", "Inv"]) < 2:
            return False
        if self.expanded and not options.checks_foodquest_expanded:
            return False
        # HARDCODE: Sofanthiel's only glow weed is in MS.  The interactive map is wrong.
        if options.starting_scug == "Inv" and options.checks_submerged < 2 and self.items[0] == "GlowWeed":
            return False
        return super().pre_generate(player, multiworld, options)


pips: list[FoodQuestPip] = [
    FoodQuestPip(0b110_111_111_000, "SlimeMold"),
    FoodQuestPip(0b110_111_111_000, "DangleFruit"),
    FoodQuestPip(0b101_111_111_000, "Fly"),
    FoodQuestPip(0b111_111_111_000, "Mushroom"),
    FoodQuestPip(0b101_011_100_000, "BlackLizard"),
    FoodQuestPip(0b110_111_111_000, "WaterNut"),
    FoodQuestPip(0b100_111_111_000, "JellyFish"),
    FoodQuestPip(0b101_011_100_000, "JetFish"),
    # Artificer can eat glow weed, but there are none in that gamestate.
    FoodQuestPip(0b110_101_111_000, "GlowWeed"),
    FoodQuestPip(0b101_011_100_000, ["Salamander", "EelLizard"]),
    FoodQuestPip(0b101_011_100_000, "Snail"),
    FoodQuestPip(0b101_111_111_000, ["Hazer", "DeadHazer"]),
    FoodQuestPip(0b101_011_100_000, "EggBug"),
    FoodQuestPip(0b110_111_111_000, "LillyPuck"),
    FoodQuestPip(0b101_011_100_000, "YellowLizard"),
    FoodQuestPip(0b101_011_100_000, "TubeWorm"),
    FoodQuestPip(0b111_111_111_000, "SSOracleSwarmer"),
    FoodQuestPip(0b101_111_111_000, "Centiwing"),
    FoodQuestPip(0b110_111_111_000, "DandelionPeach"),
    FoodQuestPip(0b101_011_100_000, "CyanLizard"),
    FoodQuestPip(0b110_111_111_000, "GooieDuck"),
    FoodQuestPip(0b101_111_111_000, ["RedCentipede", "AquaCenti"]),

    FoodQuestPip(0b111_111_111_000, "SeedCob"),
    FoodQuestPip(0b101_111_111_000, ["Centipede", "SmallCentipede"], "Centipede"),
    FoodQuestPip(0b101_111_111_000, ["VultureGrub", "DeadVultureGrub"]),
    FoodQuestPip(0b101_111_111_000, ["SmallNeedleWorm", "BigNeedleWorm"], "Noodlefly"),
    FoodQuestPip(0b101_011_100_000, "GreenLizard"),
    FoodQuestPip(0b101_011_100_000, "BlueLizard"),
    FoodQuestPip(0b101_011_100_000, "PinkLizard"),
    FoodQuestPip(0b101_011_100_000, "WhiteLizard"),
    FoodQuestPip(0b101_011_100_000, "RedLizard"),
    FoodQuestPip(0b101_011_100_000, "SpitLizard"),
    FoodQuestPip(0b100_000_000_000, "ZoopLizard"),
    FoodQuestPip(0b100_000_000_000, "TrainLizard"),
    FoodQuestPip(0b101_011_100_000, "BigSpider"),
    FoodQuestPip(0b101_011_100_000, "SpitterSpider"),
    FoodQuestPip(0b101_011_100_000, "MotherSpider"),
    # All vultures are Miros for Sofanthiel.  There are no Miros for Hunter/Gourmand.
    FoodQuestPip(0b001_011_100_000, "Vulture"),
    FoodQuestPip(0b001_011_100_000, "KingVulture"),
    FoodQuestPip(0b101_010_000_000, "MirosVulture"),
    FoodQuestPip(0b101_011_100_000, "LanternMouse"),
    FoodQuestPip(0b101_011_100_000, ["CicadaA", "CicadaB"], "Squidcada"),
    FoodQuestPip(0b100_001_000_000, "Yeek"),
    FoodQuestPip(0b101_011_100_000, "DropBug"),
    FoodQuestPip(0b101_011_100_000, "MirosBird"),
    FoodQuestPip(0b101_011_100_000, ["Scavenger", "ScavengerElite"], "Scavenger"),
    FoodQuestPip(0b101_011_100_000, ["DaddyLongLegs", "BrotherLongLegs", "TerrorLongLegs", "HunterDaddy"], "Rot"),
    FoodQuestPip(0b001_000_000_000, "PoleMimic"),
    FoodQuestPip(0b001_000_000_000, "TentaclePlant"),
    FoodQuestPip(0b001_000_000_000, "BigEel"),
    FoodQuestPip(0b001_000_000_000, "Inspector"),
]

for i in range(22, len(pips)):
    pips[i].expanded = True


def generate(options: RainWorldOptions) -> list[LocationData]:
    if options.msc_enabled and (options.starting_scug == "Gourmand") + options.checks_foodquest.value > 1:
        return pips
    return []
