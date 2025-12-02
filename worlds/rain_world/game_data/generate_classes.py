from typing import Optional

ALL_SCUGS = {'White', 'Yellow', 'Red', 'Rivulet', 'Artificer', 'Saint', 'Gourmand', 'Spear', 'Inv', 'Watcher'}


# From WorldLoader.CreatureTypeFromString()
critname_dict = {
    'aquacentipede': 'AquaCenti',
    'aquacenti': 'AquaCenti',
    'aquapede': 'AquaCenti',
    'caramel': 'SpitLizard',
    'spitlizard': 'SpitLizard',
    'strawberry': 'ZoopLizard',
    'zooplizard': 'ZoopLizard',
    'train': 'TrainLizard',
    'trainlizard': 'TrainLizard',
    'eel': 'EelLizard',
    'eellizard': 'EelLizard',
    'terror': 'TerrorLongLegs',
    'terrorlonglegs': 'TerrorLongLegs',
    'mother': 'TerrorLongLegs',
    'motherlonglegs': 'TerrorLongLegs',
    'motherspider': 'MotherSpider',
    'mirosvulture': 'MirosVulture',
    'hunterdaddy': 'HunterDaddy',
    'hunter': 'HunterDaddy',
    'hellbug': 'FireBug',
    'firebug': 'FireBug',
    'stowawaybug': 'StowawayBug',
    'scavengerelite': 'ScavengerElite',
    'elitescavenger': 'ScavengerElite',
    'elite': 'ScavengerElite',
    'inspector': 'Inspector',
    'yeek': 'Yeek',
    'bigjelly': 'BigJelly',
    'slugnpc': 'SlugNPC',
    'slugcatnpc': 'SlugNPC',

    'pink': 'PinkLizard',
    'pinklizard': 'PinkLizard',
    'green': 'GreenLizard',
    'greenlizard': 'GreenLizard',
    'blue': 'BlueLizard',
    'bluelizard': 'BlueLizard',
    'yellow': 'YellowLizard',
    'yellowlizard': 'YellowLizard',
    'white': 'WhiteLizard',
    'whitelizard': 'WhiteLizard',
    'red': 'RedLizard',
    'redlizard': 'RedLizard',
    'black': 'BlackLizard',
    'blacklizard': 'BlackLizard',
    'cyan': 'CyanLizard',
    'cyanlizard': 'CyanLizard',
    'leech': 'Leech',
    'sealeech': 'SeaLeech',
    'snail': 'Snail',
    'vulture': 'Vulture',
    'cicadaa': 'CicadaA',
    'cicadab': 'CicadaB',
    'cicada': 'CicadaA',
    'lanternmouse': 'LanternMouse',
    'mouse': 'LanternMouse',
    'spider': 'Spider',
    'worm': 'GarbageWorm',
    'garbageworm': 'GarbageWorm',
    'leviathan': 'BigEel',
    'lev': 'BigEel',
    'bigeel': 'BigEel',
    'tube': 'TubeWorm',
    'tubeworm': 'TubeWorm',
    'daddy': 'DaddyLongLegs',
    'daddylonglegs': 'DaddyLongLegs',
    'bro': 'BrotherLongLegs',
    'brolonglegs': 'BrotherLongLegs',
    'tentacleplant': 'TentaclePlant',
    'tentacle': 'TentaclePlant',
    'polemimic': 'PoleMimic',
    'mimic': 'PoleMimic',
    'mirosbird': 'MirosBird',
    'miros': 'MirosBird',
    'centipede': 'Centipede',
    'cent': 'Centipede',
    'jetfish': 'JetFish',
    'eggbug': 'EggBug',
    'bigspider': 'BigSpider',
    'spitterspider': 'SpitterSpider',
    'needleworm': 'BigNeedleWorm',
    'needle': 'BigNeedleWorm',
    'bigneedle': 'BigNeedleWorm',
    'bigneedleworm': 'BigNeedleWorm',
    'smallneedle': 'SmallNeedleWorm',
    'smallneedleworm': 'SmallNeedleWorm',
    'dropbug': 'DropBug',
    'dropwig': 'DropBug',
    'kingvulture': 'KingVulture',
    'redcentipede': 'RedCentipede',
    'redcenti': 'RedCentipede',

    'jungleleech': 'JungleLeech',
    'centipedesmall': 'NONE',

    'scavenger': 'Scavenger',
    'none': 'NONE',
    'smallcentipede': 'SmallCentipede',
    'centiwing': 'Centiwing',
    'salamander': 'Salamander',
    'deer': 'RainDeer',
    'overseer': 'Overseer',
    
    'barnacle': 'Barnacle',
    'drillcrab': 'DrillCrab',
    'sandgrub': 'SandGrub',
    'bigsandgrub': 'BigSandGrub',
    'bigmoth': 'BigMoth',
    'big moth': 'BigMoth',
    'smallmoth': 'SmallMoth',
    'small moth': 'SmallMoth',
    'boxworm': 'BoxWorm',
    'firesprite': 'FireSprite',
    'rattler': 'Rattler',
    'sky whale': 'SkyWhale',
    'skywhale': 'SkyWhale',
    'scavengertemplar': 'ScavengerTemplar',
    'templarscavenger': 'ScavengerTemplar',
    'scavenger templar': 'ScavengerTemplar',
    'templar scavenger': 'ScavengerTemplar',
    'templar': 'ScavengerTemplar',
    'scavengerdisciple': 'ScavengerDisciple',
    'disciplescavenger': 'ScavengerDisciple',
    'scavenger disciple': 'ScavengerDisciple',
    'disciple scavenger': 'ScavengerDisciple',
    'disciple': 'ScavengerDisciple',
    'loach': 'Loach',
    'rotbehemoth': 'RotLoach',
    'rot behemoth': 'RotLoach',
    'rbehemoth': 'RotLoach',
    'behemoth': 'RotLoach',
    'bigrot': 'RotLoach',
    'blizzard lizard': 'BlizzardLizard',
    'blizard': 'BlizzardLizard',
    'blizzard': 'BlizzardLizard',
    'basilisk lizard': 'BasiliskLizard',
    'basilisk': 'BasiliskLizard',
    'indigo lizard': 'IndigoLizard',
    'indigo': 'IndigoLizard',
    'skink': 'IndigoLizard',
    'rat': 'Rat',
    'frog': 'Frog',
    'tardigrade': 'Tardigrade',
    'seapig': 'Tardigrade',
}


class Crit:
    def __init__(self, s, lineage: bool):
        name, remainder = (s+"-").split('-', 1)

        self.type = critname_dict[name.lower().replace(" ", "")]
        self.attributes = []
        self.lineage_chance = 0
        self.count = 1

        while True:
            try:
                i = remainder.index("{")
                j = remainder.index("}")
                self.attributes.append(remainder[i+1:j])
                remainder = remainder[:i] + remainder[j+1:]
            except ValueError:
                break

        parts = remainder.split('-')

        for part in parts:
            if len(part) > 0:
                if part.startswith('{'):
                    self.attributes.append(part[1:-1])
                elif lineage:
                    try:
                        self.lineage_chance = float(part)
                    except ValueError:
                        pass
                else:
                    try:
                        self.count = int(part)
                    except ValueError:
                        pass

    def __repr__(self):
        return (f"{self.type}"
                f"{f' x{self.count}' if self.count > 1 else ''}"
                f"{f' / {self.attributes}' if len(self.attributes) > 0 else ''}"
                f"{f' / {self.lineage_chance}' if self.lineage_chance > 0 else ''}")


class Spawner:
    crits: list[Crit]
    room: Optional[str]

    def __init__(self, scuglist, room, den_number, critstring, lineage: bool):
        self.scugs = ALL_SCUGS
        self.update_scuglist(scuglist)
        self.room = room
        self.den_number = den_number
        self.crits = [Crit(s, lineage) for s in critstring.split(', ')]
        self.lineage = lineage

    def __repr__(self):
        return f"{self.scugstring()} : {self.room} : {self.crits}"

    def update_scuglist(self, s: str):
        if s is None:
            self.scugs = ALL_SCUGS
        elif s.startswith('X-'):
            self.scugs = self.scugs - set(s[2:].split(','))
        else:
            self.scugs = set(s.split(','))

    def scugstring(self):
        if self.scugs == ALL_SCUGS:
            return "ALL"
        elif len(self.scugs) > len(ALL_SCUGS) / 2:
            return 'X-' + ','.join(list(ALL_SCUGS - self.scugs))
        else:
            return ','.join(self.scugs)

    def has(self, crit, check_lineage: bool):
        if not check_lineage:
            return self.crits[0].type == crit
        else:
            return any([c.type == crit for c in self.crits])

    def count(self, crit):
        if self.lineage:
            return 1 if any(c.type == crit for c in self.crits) else 0
        else:
            return sum([c.count for c in self.crits if c.type == crit])

    def attr(self, s):
        return s in self.crits[0].attributes

    @property
    def den(self):
        return f"{self.room}.{self.den_number}"

    @property
    def region(self):
        return self.room[:2]
