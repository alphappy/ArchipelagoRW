#################################################################
# REGION DATA
region_code_to_name = {
    "SU": "Outskirts",
    "HI": "Industrial Complex",
    "DS": "Drainage System",
    "GW": "Garbage Wastes",
    "SL": "Shoreline",
    "VS": "Pipeyard",
    "SH": "Shaded Citadel",
    "UW": "The Exterior",
    "SS": "Five Pebbles",
    "CC": "Chimney Canopy",
    "SI": "Sky Islands",
    "LF": "Farm Arrays",
    "SB": "Subterranean",
    "MS": "Submerged Superstructure",
    "OE": "Outer Expanse",
    "LC": "Metropolis",
    "DM": "Looks to the Moon",
    "CL": "Silent Construct",
    "RM": "The Rot",
    "UG": "Undergrowth",
    "LM": "Waterfront Facility",
    "HR": "Rubicon",

    "SU^": "Outskirts filtration",
    "SL^": "Shoreline above Moon",
    "SS^": "Five Pebbles above puppet",
    "SB^": "Subterranean ravine",
    "MS^": "Bitter Aerie",
    "OE^": "Outer Expanse filtration",
    "LM^": "Eastern Precipice",

    'WARA': 'Shattered Terrace',
    'WARB': 'Salination',
    'WARC': 'Fetid Glen',
    'WARD': 'Cold Storage',
    'WARE': 'Heat Ducts',
    'WARF': 'Aether Ridge',
    'WARG': 'The Surface',
    'WAUA': 'Ancient Urban',
    'WBLA': 'Badlands',
    'WDSR': 'Decaying Tunnels',
    'WGWR': 'Infested Wastes',
    'WHIR': 'Corrupted Factories',
    'WORA': 'Outer Rim',
    'WPTA': 'Signal Spires',
    'WRFA': 'Coral Caves',
    'WRFB': 'Turbulent Pump',
    'WRRA': 'Rusted Wrecks',
    'WRSA': 'Daemon',
    'WSKA': 'Torrential Railways',
    'WSKB': 'Sunbaked Alley',
    'WSKC': 'Stormy Coast',
    'WSKD': 'Shrouded Stacks',
    'WSSR': 'Unfortunate Evolution',
    'WSUR': 'Crumbling Fringes',
    'WTDA': 'Torrid Desert',
    'WTDB': 'Desolate Tract',
    'WVWA': 'Verdant Waterways',
    'WPGA': 'Pillar Grove',
    'WMPA': 'Migration Path',
    'WVWB': 'Fractured Gateways'
}

regions_all = list(region_code_to_name.keys())

story_regions_vanilla = {"SU", "HI", "DS", "GW", "SL", "SH", "UW", "SS", "CC", "SI", "LF", "SB"}

all_regions = {
    "Vanilla": {scug: story_regions_vanilla for scug in ["Yellow", "White", "Red"]},
    "MSC": {
        "Yellow": story_regions_vanilla.union({"VS", "OE"}),
        "White": story_regions_vanilla.union({"VS", "OE"}),
        "Red": story_regions_vanilla.union({"VS"}),
        "Gourmand": story_regions_vanilla.union({"VS", "OE"}),
        "Artificer": story_regions_vanilla.union({"VS", "LC"}),
        "Rivulet": story_regions_vanilla.union({"VS", "MS"}),
        "Spear": story_regions_vanilla.union({"VS", "DM"}),
        "Saint": story_regions_vanilla.union({"VS", "HR"}).difference({"UW", "SS"}),
        "Inv": story_regions_vanilla.union({"VS"}),
    }
}
all_regions["Watcher"] = all_regions["Vanilla"]
all_regions["MSC_Watcher"] = all_regions["MSC"]

gates_vanilla = {
    "SU_HI", "SU_DS", "LF_SU", "HI_GW", "HI_CC", "HI_SH", "DS_GW", "GW_SL", "DS_SB",
    "SH_SL", "SB_SL", "SH_UW", "CC_UW", "SS_UW", "UW_SS", "SI_CC", "SI_LF", "LF_SB"
}

gates_msc_red = gates_vanilla.union({"HI_VS", "GW_SH", "DS_CC", "SL_VS", "SL_MS", "MS_SL", "SI_VS", "SB_VS", "UW_SL"})

accessible_gates = {
    "Vanilla": {
        **{scug: gates_vanilla for scug in ["Yellow", "White", "Red"]},
        "Watcher": set()
    },
    "MSC": {
        "Yellow": gates_vanilla.union(gates_msc_red).union({"SB_OE", "OE_SU"}),
        "White": gates_vanilla.union(gates_msc_red).union({"SB_OE", "OE_SU"}),
        "Red": gates_vanilla.union(gates_msc_red),
        "Gourmand": gates_vanilla.union(gates_msc_red).union({"SB_OE", "OE_SU"}),
        "Artificer": gates_vanilla.union(gates_msc_red).union({"UW_LC"}).difference({"SL_MS", "MS_SL"}),
        "Rivulet": gates_vanilla.union(gates_msc_red),
        "Spear": gates_vanilla.union(gates_msc_red).union({"SL_DM", "DM_SL"}).difference({"SL_MS", "MS_SL"}),
        "Saint": gates_vanilla.union(gates_msc_red).union({"SL_CL"}).difference(
            {"SH_SL", "UW_SS", "SS_UW", "CC_UW", "SH_UW"}
        ),
        "Inv": gates_vanilla.union(gates_msc_red),
        "Watcher": set()
    }
}
accessible_gates["MSC_Watcher"] = accessible_gates["MSC"]
accessible_gates["Watcher"] = accessible_gates["Vanilla"]

story_regions_msc = story_regions_vanilla.union({"VS"})
story_regions_gourmand = story_regions_msc.union({"OE"})
story_regions_artificer = story_regions_msc.union({"LC", "LM"}).difference({"SL"})
story_regions_rivulet = story_regions_msc.union({"RM", "MS"}).difference({"SS"})
story_regions_spearmaster = story_regions_msc.union({"DM", "LM"}).difference({"SL"})
story_regions_saint = story_regions_msc.union({"UG", "CL", "HR"}).difference({"DS", "SH", "UW", "SS"})

story_regions_watcher = {
    'WARB', 'WARC', 'WARD', 'WARE', 'WARF', 'WARG', 'WBLA', 'WMPA', 'WPGA', 'WPTA', 'WRFA', 'WRFB',
    'WRRA', 'WSKA', 'WSKB', 'WSKC', 'WSKD', 'WTDA', 'WTDB', 'WVWA', 'WVWB'
}

alternate_regions = {
    "DS": {"Saint": "UG"},
    "SH": {"Saint": "CL"},
    "SL": {"Artificer": "LM", "Spear": "LM"},
    "SS": {"Rivulet": "RM", "Saint": None},
    "UW": {"Saint": None},
}

direct_alternate_regions = {"DS": ["UG"], "SH": ["CL"], "SL": ["LM"], "SS": ["RM"]}

#################################################################
# SCUG DATA
scugs_vanilla = ['Yellow', 'White', 'Red']
scugs_msc = ['Yellow', 'White', 'Red', 'Gourmand', 'Artificer', 'Rivulet', 'Spear', 'Saint', 'Inv']
scugs_watcher = {"Yellow", "White", "Red", "Watcher"}
scugs_msc_watcher = ['Yellow', 'White', 'Red', 'Gourmand', 'Artificer', 'Rivulet', 'Spear', 'Saint', 'Inv', "Watcher"]
scugs_all = ['Yellow', 'White', 'Red', 'Gourmand', 'Artificer', 'Rivulet', 'Spear', 'Saint', 'Inv', "Watcher"]

#################################################################
# PASSAGE DATA
passages_vanilla = ["Chieftain", "DragonSlayer", "Friend", "Hunter", "Monk",
                    "Outlaw", "Saint", "Scholar", "Survivor", "Traveller"]
passages_all = ["Chieftain", "DragonSlayer", "Friend", "Hunter", "Martyr", "Monk", "Mother",
                "Nomad", "Outlaw", "Pilgrim", "Saint", "Scholar", "Survivor", "Traveller"]

passage_proper_names = {p: f"The {p}" for p in passages_all}
passage_proper_names.update({"DragonSlayer": "The Dragon Slayer", "Traveller": "The Wanderer"})

# Passages that can't be automatically set as priority until early logic detection improves.
prioritizable_passages = set(passages_all) - {"Chieftain", "Traveller", "Mother"}

dragonslayer_vanilla = {"GreenLizard", "PinkLizard", "BlueLizard", "WhiteLizard", "YellowLizard", "BlackLizard"}
dragonslayer_msc = dragonslayer_vanilla.union({"CyanLizard", "RedLizard", "SpitLizard", "ZoopLizard"})
lizards_any = dragonslayer_msc.union({"Salamander", "EelLizard", "TrainLizard"})

echoes_vanilla = ['CC', 'SI', 'LF', 'SB', 'SH', 'UW']

monk_foods_vanilla = ['DangleFruit', 'BubbleFruit', 'SeedCob', 'SlimeMold', 'SSOracleSwarmer']
monk_foods_msc = ['LillyPuck', 'GlowWeed', 'DandelionPeach', 'GooieDuck', 'Seed', 'FireEgg']
monk_foods_watcher = ['Pomegranate']

slugpup_normal_regions = ['HI', 'DS', 'GW', 'SH', 'CC', 'SI', 'LF', 'SB', 'VS']

outlaw_whitelist = lizards_any.union({
    "BigSpider", "SpitterSpider", "MotherSpider", "Scavenger", "EliteScavenger", "Vulture", "KingVulture",
    "MirosVulture", "MirosBird", "Centipede", "RedCentipede", "Aquapede", "BigNeedleWorm", "CicadaA", "CicadaB"
})

scavenger_tolls = ["SU", "GW", "LF", "LC", "CL", "OE", "UG"]

# Certain hard to reach pearls omitted to not overcomplicate scholar with location access rules (WTDB, WMPA, WARG)
watcher_pearls = ["WBLA", "WARD", "WARC", "WARE", "WARB", "WSKD", "WPTA", "WTDA", "WRFB", "WVWA"]

#################################################################
# FOOD QUEST DATA

food_quest_items = [
    "SlimeMold", "DangleFruit", "Fly", "Mushroom", "BlackLizard", "WaterNut",
    "JellyFish", "JetFish", "GlowWeed", "Salamander", "Snail", "Hazer",
    "EggBug", "LillyPuck", "YellowLizard", "TubeWorm", "SSOracleSwarmer", "Centiwing",
    "DandelionPeach", "CyanLizard", "GooieDuck", "RedCentipede"
]
alt_food_quest_items = {"Salamander": ["Salamander", "EelLizard"], "RedCentipede": ["RedCentipede", "AquaCenti"]}

food_quest_survivor_inedible = {
    "BlackLizard", "JetFish", "Salamander", "Snail", "EggBug", "YellowLizard", "TubeWorm", "CyanLizard"
}
food_quest_spearmaster_inedible = {
    "SlimeMold", "DangleFruit", "WaterNut", "JellyFish", "GlowWeed", "LillyPuck", "DandelionPeach", "GooieDuck"
}
food_quest_saint_inedible = {
    "Fly", "BlackLizard", "JellyFish", "JetFish", "Salamander", "Snail", "Hazer", "EggBug", "YellowLizard", "TubeWorm",
    "Centiwing", "CyanLizard", "RedCentipede"
}

extreme_threat_creatures = {
    "BrotherLongLegs", "DaddyLongLegs", "TerrorLongLegs", "HunterDaddy", "RedLizard", "RedCentipede",
    "KingVulture", "MirosVulture", "MirosBird", "AquaCenti"
}

#################################################################
# WIKI NAMES
wiki_names = {
    "LizardTemplate": ["Lizards"],
    "GreenLizard": ["Green Lizard"],
    "PinkLizard": ["Pink Lizard"],
    "BlueLizard": ["Blue Lizard"],
    "WhiteLizard": ["White Lizard"],
    "BlackLizard": ["Black Lizard"],
    "YellowLizard": ["Yellow Lizard"],
    "SpitLizard": ["Caramel Lizard"],
    "ZoopLizard": ["Strawberry Lizard"],
    "CyanLizard": ["Cyan Lizard"],
    "RedLizard": ["Red Lizard"],
    "Salamander": ["Salamander"],
    "EelLizard": ["Eel Lizard"],
    "TrainLizard": ["Train Lizard"],
    "Centipede": ["Centipede"],
    "SmallCentipede": ["Infant Centipede"],
    "Centiwing": ["Centiwing"],
    "AquaCenti": ["Aquapede"],
    "RedCentipede": ["Red Centipede"],
    "Spider": ["Coalescipede"],
    "BigSpider": ["Big Spider"],
    "MotherSpider": ["Mother Spider"],
    "SpitterSpider": ["Spitter Spider"],
    "VultureGrub": ["Vulture Grub"],
    "Vulture": ["Vulture"],
    "KingVulture": ["King Vulture"],
    "MirosBird": ["Miros Bird"],
    "MirosVulture": ["Miros Vulture"],
    "DaddyLongLegs": ["Daddy Long Legs"],
    "BrotherLongLegs": ["Brother Long Legs"],
    "TerrorLongLegs": ["Mother Long Legs"],
    "HunterDaddy": ["Hunter Long Legs"],
    "Inspector": ["Inspector"],
    "Leech": ["Red Leech"],
    "SeaLeech": ["Blue Leech"],
    "JungleLeech": ["Jungle Leech"],
    "Scavenger": ["Scavenger"],
    "ScavengerElite": ["Elite Scavenger"],
    "ScavengerKing": ["Chieftain Scavenger"],
    "TempleGuard": ["Guardian"],
    "Fly": ["Batfly"],
    "CicadaB": ["Black Squidcada"],
    "DropBug": ["Dropwig"],
    "EggBug": ["Eggbug"],
    "GarbageWorm": ["Garbage Worm"],
    "TubeWorm": ["Grappling Worm", "Tube Worm"],
    "Hazer": ["Hazer"],
    "JellyFish": ["Jellyfish"],
    "JetFish": ["Jetfish"],
    "LanternMouse": ["Lantern Mouse"],
    "BigEel": ["Leviathan"],
    "TentaclePlant": ["Monster Kelp"],
    "BigNeedleWorm": ["Adult Noodlefly"],
    "SmallNeedleWorm": ["Infant Noodlefly"],
    "Overseer": ["Overseer"],
    "PoleMimic": ["Pole Plant", "Pole Mimic"],
    "Deer": ["Rain Deer", "Deer"],
    "Slugcat": ["Slugcat"],
    "Snail": ["Snail"],
    "CicadaA": ["White Squidcada"],
    "FireBug": ["Firebug", "Hellbug"],
    "StowawayBug": ["Stowaway"],
    "Yeek": ["Yeek"],
    "BigJelly": ["Giant Jellyfish", "Big Jellyfish"],
    "ReliableSpear": ["Spear"],
    "Spear": ["Spear"],
    "ExplosiveSpear": ["Explosive Spear"],
    "ElectricSpear": ["Electric Spear"],
    "FireSpear": ["Fire Spear"],
    "VultureMask": ["Vulture Mask"],
    "SSOracleSwarmer": ["Neuron Fly"],
    "ScavengerBomb": ["Grenade", "Bomb"],
    "SingularityBomb": ["Singularity Bomb"],
    "Rock": ["Rock"],
    "DangleFruit": ["Blue Fruit"],
    "SlimeMold": ["Slime Mold"],
    "GooieDuck": ["Gooieduck"],
    "LillyPuck": ["Lilypuck"],
    "EggBugEgg": ["Eggbug Egg"],
    "NeedleEgg": ["Noodlefly Egg"],
    "FlyLure": ["Batnip"],
    "BubbleGrass": ["Bubble Weed"],
    "SporePlant": ["Beehive"],
    "FirecrackerPlant": ["Cherrybomb", "Firecracker"],
    "FlareBomb": ["Flashbang"],
    "PuffBall": ["Spore Puff"],
    "MoonCloak": ["Cloak"],
    "EnergyCell": ["Rarefaction Cell", "Energy Cell"],
    "JokeRifle": ["Joke Rifle", "Gun", "Rifle"],
    "Mushroom": ["Mushroom"],
    "WaterNut": ["Bubble Fruit"],
    "GlowWeed": ["Glow Weed"],
    "DandelionPeach": ["Dandelion Peach"],
    "DeadHazer": ["Hazer"],
    "DeadVultureGrub": ["VultureGrub"],
    "SeedCob": ["Popcorn Plant"],
    # Watcher
    "Barnacle": ["Barnacle"],
    "SandGrub": ["Sand Grub"],
    "BigSandGrub": ["Sand Worm"],
    "BigMoth": ["Big Moth"],
    "SmallMoth": ["Small Moth"],
    "BoxWorm": ["Box Worm"],
    "FireSprite": ["Fire Sprite"],
    "Rattler": ["Rattler", "Bone Shaker"],
    "SkyWhale": ["Sky Whale"],
    "ScavengerTemplar": ["Scavenger Templar"],
    "ScavengerDisciple": ["Scavenger Disciple"],
    "Loach": ["Loach"],
    "RotLoach": ["Rot Loach"],
    "BlizzardLizard": ["Blizzard Lizard"],
    "BasiliskLizard": ["Basilisk Lizard"],
    "IndigoLizard": ["Indigo Lizard"],
    "PeachLizard": ["Peach Lizard"],
    "Rat": ["Rat"],
    "Frog": ["Frog"],
    "Tardigrade": ["Tardigrade"],
    "Angler": ["Angler"],
    "RippleSpider": ["Ripple Spider"],
    "MothGrub": ["Moth Grub"],
    "FireSpriteLarva": ["Fire Sprite Larva"],
    "SandGrubNetwork": ["Sand Grub"],
    "PlacedRats": ["Rat"],
    "Pomegranate": ["Pomegranate"],
    # The presence of a box worm is used to indicate Fire Sprite Larva access for food quest.
    # So while not technically accurate, this translates what we check for into the readable name
    "PlacedBoxWorm": ["Fire Sprite Larva"],
}
