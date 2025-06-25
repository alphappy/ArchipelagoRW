from BaseClasses import Region, MultiWorld
from ..options import RainWorldOptions
from ..conditions.classes import Condition, ConditionBlank, Simple, AnyOf, AllOf
from ..utils_ap import try_get_region


class RainWorldRegion(Region):
    game = "Rain World"

    def __init__(self, name: str, player: int, multiworld: MultiWorld, populate: bool,
                 rooms: set[str] | None = None, code: str = ""):
        super().__init__(name, player, multiworld)
        self.populate, self.rooms, self.code = populate, rooms, code


class RegionData:
    def __init__(self, name: str, populate: bool = True):
        self.name, self.populate = name, populate

    def make(self, player: int, multiworld: MultiWorld, _: RainWorldOptions):
        multiworld.regions.append(RainWorldRegion(self.name, player, multiworld, self.populate))


class ConnectionData:
    """
    Represents a connection between Archi regions.
    """
    def __init__(self, source: str, dest: str, name: str, condition: Condition = ConditionBlank):
        self.source, self.dest, self.name, self.condition = source, dest, name, condition

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        source = try_get_region(multiworld, self.source, player)
        dest = try_get_region(multiworld, self.dest, player)
        if source and dest:
            source.connect(dest, self.name, rule=self.condition.check(player))


class Gate(ConnectionData):
    """
    Represents a karma gate connection between actual regions.
    """
    def __init__(self, source: str, dest: str, cost: int, gate_name: str, condition: Condition = ConditionBlank):
        super().__init__(source, dest, "")
        self.cost = cost
        self.gate_name = gate_name
        self.condition = condition

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        source = multiworld.get_region(self.source, player)
        dest = multiworld.get_region(self.dest, player)

        karma_items = self.cost - (1 if self.cost < 6 else 2)

        match options.which_gate_behavior:
            case "key_only":
                rule = Simple(f"GATE_{self.gate_name}")
            case "karma_only":
                rule = Simple("Karma", karma_items)
            case "key_and_karma":
                rule = AllOf(Simple(f"GATE_{self.gate_name}"), Simple("Karma", karma_items))
            case "key_or_karma":
                rule = AnyOf(Simple(f"GATE_{self.gate_name}"), Simple("Karma", karma_items))
            case _:
                raise ValueError(f"{options.which_gate_behavior} is not a valid value for `which_gate_behavior`")

        rule = AllOf(rule, self.condition)
        source.connect(dest, name=f'GATE_{self.gate_name} ({self.source} to {dest.name})', rule=rule.check(player))


room_to_region: dict[str, str] = dict()


class PhysicalRegion(RegionData):
    def __init__(self, name: str, prefix: str, rooms: set[str]):
        super().__init__(name, True)
        self.prefix, self.rooms = prefix, rooms

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        self.populate = self._gen(options)
        room_to_region.update({room: self.name for room in self.rooms})
        if self.populate:
            region = RainWorldRegion(self.name, player, multiworld, self.populate, self.rooms, self.prefix)
            multiworld.regions.append(region)

    def _gen(self, options: RainWorldOptions) -> bool:
        rcode, scug = self.prefix.split("^")[0], options.starting_scug

        if scug == "Watcher":
            if len(rcode) == 4 and rcode[0] == "W":
                if options.logic_rotted_generation != 3 and rcode in ["WSUR", "WHIR", "WDSR", "WGWR"]:
                    return False
                return True
            return False

        match rcode:
            case "SU":
                # HARDCODE
                if self.name in ("Spearmaster spawn area", "Outskirts filtration"):
                    return scug in ("Yellow", "White", "Gourmand", "Spear") and options.msc_enabled
                if self.name not in ("Outskirts", "Survivor tutorial area"):
                    return options.msc_enabled and scug in ("Yellow", "White", "Gourmand")
                return True
            case "HI" | "GW" | "CC" | "SI" | "LF" | "SB":
                return True
            case "DS" | "SH" | "UW":
                return scug != "Saint"
            case "SS":
                return scug not in ("Saint", "Rivulet")
            case "SL":
                # HARDCODE
                if self.name == "Shoreline above puppet":
                    return scug in ("Rivulet", "Saint")
                if self.name == "Broken Precipice":
                    return options.msc_enabled and scug not in ("Artificer", "Spear", "Saint")
                return scug not in ("Artificer", "Spear")

        if not options.msc_enabled:
            return False

        match rcode:
            case "VS":
                return True
            case "OE":
                return scug in ("Yellow", "White", "Gourmand")
            case "LC":
                return scug == "Artificer"
            case "LM":
                return scug in ("Artificer", "Spear")
            case "RM":
                return scug == "Rivulet"
            case "DM":
                return scug == "Spear"
            case "UG" | "HR" | "CL":
                return scug == "Saint"
            case "MS":
                # HARDCODE
                if self.name == "Bitter Aerie":
                    return scug == "Rivulet"
                return scug not in ("Artificer", "Spear")
