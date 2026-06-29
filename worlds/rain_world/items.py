from BaseClasses import Item, ItemClassification
from typing import Optional, Dict
from . import constants, game_data
from .regions.gates import gates
from .game_data.general import region_code_to_name, alternate_regions
from .game_data.watcher import keys as pkeys, normal_regions, PortalKeyData

item_client_names: dict[str, str] = {}


class RainWorldItem(Item):
    game: str = "Rain World"


class RainWorldItemData:
    def __init__(self, name: str, client_name: str, code: Optional[int],
                 item_type: ItemClassification = ItemClassification.filler):
        self.name = name
        self.client_name = client_name
        self.hints: list[str] = []
        self.code = code
        self.item_type = item_type
        item_client_names[client_name] = name

    def generate_item(self, player: int) -> RainWorldItem:
        return RainWorldItem(self.name, self.item_type, self.code, player)


class GateKeyItemData(RainWorldItemData):
    def __init__(self, names: list[str], code: Optional[int]):
        super().__init__(names[0], names[-1], code, ItemClassification.progression)
        _, left_code, right_code = names[-1].split("_")
        self.hints = names[1:] + [region_code_to_name[left_code], region_code_to_name[right_code]]


class PortalKeyItemData(RainWorldItemData):
    def __init__(self, data: PortalKeyData, code: Optional[int]):
        super().__init__(data.name, data.client_name, code, ItemClassification.progression)
        _, left_code, right_code = data.client_name.split("-")
        self.spinning_top = data.spinning_top
        self.hints = [data.client_name, region_code_to_name[left_code], region_code_to_name[right_code]]


class PassageTokenItemData(RainWorldItemData):
    def __init__(self, name: str, client_name: str, code: Optional[int]):
        super().__init__(name, client_name, code, ItemClassification.useful)
        self.hints = ["Passage Token"]


class FillerItemData(RainWorldItemData):
    def __init__(self, name: str, client_name: str, code: Optional[int], gamestate: Optional[list[str]] = None):
        super().__init__(name, client_name, code, ItemClassification.filler)
        self.gamestate = gamestate or []


class TrapItemData(RainWorldItemData):
    def __init__(self, name: str, client_name: str, code: Optional[int], gamestate: Optional[list[str]] = None):
        super().__init__(name, client_name, code, ItemClassification.trap)
        self.gamestate = gamestate or []


offset: int = constants.FIRST_ID

all_items: Dict[str, RainWorldItemData] = {
    #################################################################
    # PROGRESSION
    "Karma": RainWorldItemData("Karma", "Karma", offset, ItemClassification.progression),
    "The Mark": RainWorldItemData("The Mark", "The Mark", offset + 1, ItemClassification.progression),
    "Citizen ID Drone": RainWorldItemData("Citizen ID Drone", "IdDrone", offset + 2, ItemClassification.progression),
    "Rarefaction Cell": RainWorldItemData("Rarefaction Cell", "Object-EnergyCell", offset + 3, ItemClassification.progression),
    "Spearmaster's Pearl": RainWorldItemData("Spearmaster's Pearl", "PearlObject-Spearmasterpearl", offset + 4, ItemClassification.progression),
    "Moon's Final Message": RainWorldItemData("Moon's Final Message", "Rewrite_Spear_Pearl", offset + 5, ItemClassification.progression),
    "Slag Key": RainWorldItemData("Slag Key", "Object-NSHSwarmer", offset + 6, ItemClassification.progression),
    "Ripple": RainWorldItemData("Ripple", "Ripple", offset + 7, ItemClassification.progression),

    #################################################################
    # PASSAGE TOKENS
    **{
        f"Passage Token - {pv}": PassageTokenItemData(
            f"Passage Token - {pv}", f"Passage-{pk}", offset + 20 + i
        )
        for i, (pk, pv) in enumerate(game_data.general.passage_proper_names.items())
    },

    #################################################################
    # UNIQUE
    "The Glow": RainWorldItemData("The Glow", "The Glow", offset + 50, ItemClassification.progression),
    "Longer cycles": RainWorldItemData("Longer cycles", "Disconnect_FP", offset + 51, ItemClassification.progression),
    "Dial Warp Ability": RainWorldItemData("Dial Warp Ability", "Dial_Warp", offset + 52, ItemClassification.progression),

    #################################################################
    # FILLER - WEAPONS
    "Rock": FillerItemData("Rock", "Object-Rock", 200 + offset),
    "Spear": FillerItemData("Spear", "Object-Spear", 201 + offset),
    "Explosive Spear": FillerItemData("Explosive Spear", "Object-ExplosiveSpear", 202 + offset),
    "Electric Spear": FillerItemData("Electric Spear", "Object-ElectricSpear", 203 + offset, ["MSC"]),
    "Grenade": FillerItemData("Grenade", "Object-ScavengerBomb", 204 + offset),
    "Flashbang": FillerItemData("Flashbang", "Object-FlareBomb", 205 + offset),
    "Spore Puff": FillerItemData("Spore Puff", "Object-PuffBall", 206 + offset),
    "Cherrybomb": FillerItemData("Cherrybomb", "Object-FirecrackerPlant", 207 + offset),
    "Singularity Bomb": FillerItemData("Singularity Bomb", "Object-SingularityBomb", 208 + offset, ["MSC"]),
    "Lilypuck": FillerItemData("Lilypuck", "Object-LillyPuck", 209 + offset, ["MSC"]),
    "Hell Spear": FillerItemData("Hell Spear", "Object-HellSpear", 210 + offset, ["MSC"]),
    "Poison Spear": FillerItemData("Poison Spear", "Object-PoisonSpear", 211 + offset, ["Watcher"]),
    "Boomerang": FillerItemData("Boomerang", "Object-Boomerang", 212 + offset, ["Watcher"]),

    #################################################################
    # FILLER - FOOD
    "Blue Fruit": FillerItemData("Blue Fruit", "Object-DangleFruit", 240 + offset),
    "Bubble Fruit": FillerItemData("Bubble Fruit", "Object-WaterNut", 241 + offset),
    "Eggbug Egg": FillerItemData("Eggbug Egg", "Object-EggBugEgg", 242 + offset),
    "Jellyfish": FillerItemData("Jellyfish", "Object-JellyFish", 243 + offset),
    "Mushroom": FillerItemData("Mushroom", "Object-Mushroom", 244 + offset),
    "Slime Mold": FillerItemData("Slime Mold", "Object-SlimeMold", 245 + offset),
    "Fire Egg": FillerItemData("Fire Egg", "Object-FireEgg", 246 + offset, ["MSC"]),
    "Glow Weed": FillerItemData("Glow Weed", "Object-GlowWeed", 247 + offset, ["MSC"]),
    "Seed": FillerItemData("Seed", "Object-Seed", 248 + offset, ["MSC"]),
    "Gooieduck": FillerItemData("Gooieduck", "Object-GooieDuck", 249 + offset, ["MSC"]),
    "Dandelion Peach": FillerItemData("Dandelion Peach", "Object-DandelionPeach", 250 + offset, ["MSC"]),
    "Rot Fruit": FillerItemData("Rot Fruit", "Object-RotFruit", 251 + offset, ["Watcher"]),
    "Fire Sprite Larva": FillerItemData("Fire Sprite Larva", "Object-FireSpriteLarva", 252 + offset, ["Watcher"]),

    #################################################################
    # FILLER - OTHER
    "Bubble Weed": FillerItemData("Bubble Weed", "Object-BubbleGrass", 270 + offset),
    "Batnip": FillerItemData("Batnip", "Object-FlyLure", 271 + offset),
    "Lantern": FillerItemData("Lantern", "Object-Lantern", 272 + offset),
    "Karma Flower": FillerItemData("Karma Flower", "Object-KarmaFlower", 273 + offset),
    "Vulture Mask": FillerItemData("Vulture Mask", "Object-VultureMask", 274 + offset),
    "Joke Rifle": FillerItemData("Joke Rifle", "Object-JokeRifle", 275 + offset, ["MSC"]),
    "Graffiti Bomb": FillerItemData("Graffiti Bomb", "Object-GraffitiBomb", 276 + offset, ["Watcher"]),
    "Pearl": FillerItemData("Pearl", "Object-DataPearl", 277 + offset),
    "Beehive": FillerItemData("Beehive", "Object-SporePlant", 278 + offset),

    #################################################################
    # FILLER - NON-CREATURE TRAPS
    "Stun Trap": TrapItemData("Stun Trap", "Trap-Stun", 300 + offset),
    "Zoomies Trap": TrapItemData("Zoomies Trap", "Trap-Zoomies", 301 + offset),
    "Timer Trap": TrapItemData("Timer Trap", "Trap-Timer", 302 + offset),
    "Rain Trap": TrapItemData("Rain Trap", "Trap-Rain", 303 + offset),
    "Gravity Trap": TrapItemData("Gravity Trap", "Trap-Gravity", 304 + offset),
    "Fog Trap": TrapItemData("Fog Trap", "Trap-Fog", 305 + offset),
    "Killsquad Trap": TrapItemData("Killsquad Trap", "Trap-KillSquad", 306 + offset),
    "Alarm Trap": TrapItemData("Alarm Trap", "Trap-Alarm", 307 + offset),

    #################################################################
    # FILLER - CREATURE TRAPS
    "Red Lizard Trap": TrapItemData("Red Lizard Trap", "Trap-RedLizard", 330 + offset),
    "Red Centipede Trap": TrapItemData("Red Centipede Trap", "Trap-RedCentipede", 331 + offset),
    "Spitter Spider Trap": TrapItemData("Spitter Spider Trap", "Trap-SpitterSpider", 332 + offset),
    "Brother Long Legs Trap": TrapItemData("Brother Long Legs Trap", "Trap-BrotherLongLegs", 333 + offset),
    "Daddy Long Legs Trap": TrapItemData("Daddy Long Legs Trap", "Trap-DaddyLongLegs", 334 + offset),
    "Responsibility Trap": TrapItemData("Responsibility Trap", "Trap-Responsibility", 335 + offset),
    "Ripple Spawn Trap": TrapItemData("Ripple Spawn Trap", "Trap-RippleSpawn", 336 + offset),
    "Blizzard Lizard Trap": TrapItemData("Blizzard Lizard Trap", "Trap-BlizzardLizard", 337 + offset),

    #################################################################
    # FILLER - UPGRADES
    "Spear Damage Increase": RainWorldItemData("Spear Damage Increase", "Upgrade-SpearDamage", 370 + offset, ItemClassification.useful),
    # FILLER - EXPEDITION PERKS
    "Back Spear Perk": RainWorldItemData("Back Spear Perk", "Exp-BackSpear", 380 + offset, ItemClassification.useful),
    "Dual Wielding Perk": RainWorldItemData("Dual Wielding Perk", "Exp-DualWielding", 381 + offset, ItemClassification.useful),
    "Blast Resistance Perk": RainWorldItemData("Blast Resistance Perk", "Exp-ExplosionResistance", 382 + offset, ItemClassification.useful),
    "Explosive Parry Perk": RainWorldItemData("Explosive Parry Perk", "Exp-ExplosiveParry", 383 + offset, ItemClassification.useful),
    "Explosive Jump Perk": RainWorldItemData("Explosive Jump Perk", "Exp-ExplosiveJump", 384 + offset, ItemClassification.useful | ItemClassification.progression),
    "Crafting Perk": RainWorldItemData("Crafting Perk", "Exp-ItemCrafting", 385 + offset, ItemClassification.useful),
    "Aquatic Perk": RainWorldItemData("Aquatic Perk", "Exp-Aquatic", 386 + offset, ItemClassification.useful | ItemClassification.progression),
    "Agility Perk": RainWorldItemData("Agility Perk", "Exp-Agility", 387 + offset, ItemClassification.useful),
}

#################################################################
# GATES
gate_keys: dict[str, GateKeyItemData] = {
    names[0]: GateKeyItemData(names, offset + 500 + i)
    for i, names in enumerate([g.names for g in gates])
}
all_items.update(gate_keys)

#################################################################
# PORTAL KEYS
portal_keys: dict[str, RainWorldItemData] = {
    data.name: PortalKeyItemData(data, offset + 600 + i)
    for i, data in enumerate(pkeys.values())
}
all_items.update(portal_keys)

#################################################################
# DYNAMIC WARP KEYS
dynamic_warp_keys: dict[str, RainWorldItemData] = {
    f"Dynamic: {r}": RainWorldItemData(f"Dynamic: {r}", f"Dynamic-{r}", offset + 700 + i, ItemClassification.progression)
    for i, r in enumerate(normal_regions)
}
all_items.update(dynamic_warp_keys)

#################################################################
item_name_to_id: Dict[str, int] = {k: v.code for k, v in all_items.items()}

item_hints: dict[str, set[str]] = {}
for item in all_items.values():
    for hint in [h for h in item.hints if h != item.name]:
        item_hints.setdefault(hint, set()).update({item.name})
