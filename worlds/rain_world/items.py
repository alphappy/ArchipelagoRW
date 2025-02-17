from BaseClasses import Item, ItemClassification
from typing import Optional, Dict
from . import constants, RainWorldOptions, game_data
from .game_data.general import gates_all


class RainWorldItem(Item):
    game: str = "Rain World"


class RainWorldItemData:
    def __init__(self, name: str, code: Optional[int], item_type: ItemClassification = ItemClassification.filler):
        self.name = name
        self.code = code
        self.item_type = item_type

    def generate_item(self, player: int) -> RainWorldItem:
        return RainWorldItem(self.name, self.item_type, self.code, player)


class FillerItemData(RainWorldItemData):
    def __init__(self, name: str, code: Optional[int], gamestate: Optional[list[str]] = None):
        super().__init__(name, code, ItemClassification.filler)
        self.gamestate = gamestate or []


offset: int = constants.FIRST_ID

all_items: Dict[str, RainWorldItemData] = {
    #################################################################
    # PROGRESSION
    "Karma": RainWorldItemData("Karma", offset, ItemClassification.progression),
    "The Mark": RainWorldItemData("The Mark", offset + 1, ItemClassification.progression),
    "IdDrone": RainWorldItemData("IdDrone", offset + 2, ItemClassification.progression),
    "Object-EnergyCell": RainWorldItemData("Object-EnergyCell", offset + 3, ItemClassification.progression),
    "PearlObject-Spearmasterpearl": RainWorldItemData("PearlObject-Spearmasterpearl", offset + 4,
                                                      ItemClassification.progression),
    "Rewrite_Spear_Pearl": RainWorldItemData("Rewrite_Spear_Pearl", offset + 5, ItemClassification.progression),
    "Object-NSHSwarmer": RainWorldItemData("Object-NSHSwarmer", offset + 6, ItemClassification.progression),

    #################################################################
    # PASSAGE TOKENS
    **{
        f"Passage-{p}": RainWorldItemData(f"Passage-{p}", offset + 20 + i, ItemClassification.useful)
        for i, p in enumerate(game_data.general.passages_all)
    },

    #################################################################
    # UNIQUE
    "The Glow": RainWorldItemData("The Glow", offset + 50, ItemClassification.progression),
    "Disconnect_FP": RainWorldItemData("Disconnect_FP", offset + 51, ItemClassification.useful),

    #################################################################
    # GAMESTATE
    "MSC": RainWorldItemData("MSC", offset + 100, ItemClassification.progression),
    "Scug-Yellow": RainWorldItemData("Scug-Yellow", offset + 110, ItemClassification.progression),
    "Scug-White": RainWorldItemData("Scug-White", offset + 111, ItemClassification.progression),
    "Scug-Red": RainWorldItemData("Scug-Red", offset + 112, ItemClassification.progression),
    "Scug-Gourmand": RainWorldItemData("Scug-Gourmand", offset + 113, ItemClassification.progression),
    "Scug-Artificer": RainWorldItemData("Scug-Artificer", offset + 114, ItemClassification.progression),
    "Scug-Rivulet": RainWorldItemData("Scug-Rivulet", offset + 115, ItemClassification.progression),
    "Scug-Spear": RainWorldItemData("Scug-Spear", offset + 116, ItemClassification.progression),
    "Scug-Saint": RainWorldItemData("Scug-Saint", offset + 117, ItemClassification.progression),
    "Scug-Inv": RainWorldItemData("Scug-Inv", offset + 118, ItemClassification.progression),

    #################################################################
    # OPTIONSTATE

    "Option-Glow": RainWorldItemData("Option-Glow", offset + 170, ItemClassification.progression),

    #################################################################
    # FILLER - WEAPONS
    "Object-Rock": FillerItemData("Object-Rock", 200 + offset),
    "Object-Spear": FillerItemData("Object-Spear", 201 + offset),
    "Object-ExplosiveSpear": FillerItemData("Object-ExplosiveSpear", 202 + offset),
    "Object-ElectricSpear": FillerItemData("Object-ElectricSpear", 203 + offset, ["MSC"]),
    "Object-ScavengerBomb": FillerItemData("Object-ScavengerBomb", 204 + offset),
    "Object-FlareBomb": FillerItemData("Object-FlareBomb", 205 + offset),
    "Object-PuffBall": FillerItemData("Object-PuffBall", 206 + offset),
    "Object-FirecrackerPlant": FillerItemData("Object-FirecrackerPlant", 207 + offset),
    "Object-SingularityBomb": FillerItemData("Object-SingularityBomb", 208 + offset, ["MSC"]),
    "Object-LillyPuck": FillerItemData("Object-LillyPuck", 209 + offset, ["MSC"]),

    #################################################################
    # FILLER - FOOD
    "Object-DangleFruit": FillerItemData("Object-DangleFruit", 240 + offset),
    "Object-WaterNut": FillerItemData("Object-WaterNut", 241 + offset),
    "Object-EggBugEgg": FillerItemData("Object-EggBugEgg", 242 + offset),
    "Object-JellyFish": FillerItemData("Object-JellyFish", 243 + offset),
    "Object-Mushroom": FillerItemData("Object-Mushroom", 244 + offset),
    "Object-SlimeMold": FillerItemData("Object-SlimeMold", 245 + offset),
    "Object-FireEgg": FillerItemData("Object-FireEgg", 246 + offset, ["MSC"]),
    "Object-GlowWeed": FillerItemData("Object-GlowWeed", 247 + offset, ["MSC"]),
    "Object-Seed": FillerItemData("Object-Seed", 248 + offset, ["MSC"]),
    "Object-GooieDuck": FillerItemData("Object-GooieDuck", 249 + offset, ["MSC"]),
    "Object-DandelionPeach": FillerItemData("Object-DandelionPeach", 250 + offset, ["MSC"]),

    #################################################################
    # FILLER - OTHER
    "Object-BubbleGrass": FillerItemData("Object-BubbleGrass", 270 + offset),
    "Object-FlyLure": FillerItemData("Object-FlyLure", 271 + offset),
    "Object-Lantern": FillerItemData("Object-Lantern", 272 + offset),
    "Object-KarmaFlower": FillerItemData("Object-KarmaFlower", 273 + offset),
    "Object-VultureMask": FillerItemData("Object-VultureMask", 274 + offset),
    "Object-JokeRifle": FillerItemData("Object-JokeRifle", 275 + offset, ["MSC"]),

    #################################################################
    # FILLER - NON-CREATURE TRAPS
    "Trap-Stun": FillerItemData("Trap-Stun", 300 + offset),
    "Trap-Zoomies": FillerItemData("Trap-Zoomies", 301 + offset),
    "Trap-Timer": FillerItemData("Trap-Timer", 302 + offset),
    "Trap-Flood": FillerItemData("Trap-Flood", 303 + offset),
    "Trap-Rain": FillerItemData("Trap-Rain", 304 + offset),
    "Trap-Gravity": FillerItemData("Trap-Gravity", 305 + offset),
    "Trap-Fog": FillerItemData("Trap-Fog", 306 + offset),
    "Trap-KillSquad": FillerItemData("Trap-KillSquad", 307 + offset),
    "Trap-Alarm": FillerItemData("Trap-Alarm", 308 + offset),

    #################################################################
    # FILLER - CREATURE TRAPS
    "Trap-RedLizard": FillerItemData("Trap-RedLizard", 330 + offset),
    "Trap-RedCentipede": FillerItemData("Trap-RedCentipede", 331 + offset),
    "Trap-SpitterSpider": FillerItemData("Trap-SpitterSpider", 332 + offset),
    "Trap-BrotherLongLegs": FillerItemData("Trap-BrotherLongLegs", 333 + offset),
    "Trap-DaddyLongLegs": FillerItemData("Trap-DaddyLongLegs", 334 + offset),
}

#################################################################
# GATES
for i, gate in enumerate(gates_all):
    all_items[f"GATE_{gate}"] = RainWorldItemData(f"GATE_{gate}", offset + 500 + i, ItemClassification.progression)

#################################################################
item_name_to_id: Dict[str, int] = {
    k: v.code for k, v in all_items.items()
}
