from typing import NamedTuple, Callable, Optional

from BaseClasses import Region, MultiWorld
from . import RainWorldOptions
from .conditions.classes import Condition, Simple, Compound, ConditionBlank, AllOf
from .conditions import generate
from .game_data.general import setting_to_scug_id


class ConnectionData:
    """
    Represents a connection between Archi regions.
    """
    def __init__(self, source: str, dest: str, condition: Condition = ConditionBlank):
        self.source = source
        self.dest = dest
        self.condition = condition

    def make(self, player: int, multiworld: MultiWorld):
        source = multiworld.get_region(self.source, player)
        dest = multiworld.get_region(self.dest, player)
        source.connect(dest, rule=self.condition.check(player))


class Gate(ConnectionData):
    """
    Represents a karma gate connection between actual regions.
    """
    def __init__(self, source: str, dest: str, cost: int, gate_name: str, condition: Condition = ConditionBlank):
        super().__init__(source, dest)
        self.cost = cost
        self.gate_name = gate_name
        self.condition = condition

    def make(self, player: int, multiworld: MultiWorld):
        source = multiworld.get_region(self.source, player)
        dest = multiworld.get_region(self.dest, player)
        conditions = [
            Simple("Karma", self.cost - (1 if self.cost < 6 else 2)),
            Simple(f"GATE_{self.gate_name}"),
            self.condition
        ]
        rule = Compound(len(conditions), *conditions)
        source.connect(dest, name=f'GATE_{self.gate_name} ({self.source} to {dest.name})', rule=rule.check(player))


class RainWorldRegion(Region):
    game = "Rain World"

    def __init__(self, name: str, player: int, multiworld: MultiWorld, populate: bool):
        super().__init__(name, player, multiworld)
        self.populate = populate


class RegionData:
    def __init__(self, full_name: str, short_name: str,
                 generation_condition: Callable[[RainWorldOptions], bool] = lambda _: True):
        self.full_name = full_name
        self.short_name = short_name
        self.generation_condition = generation_condition

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        multiworld.regions.append(RainWorldRegion(
            self.full_name, player, multiworld, self.generation_condition(options))
        )


def any_scug_except(scugs: list[str]) -> Simple:
    return Simple([f"Scug-{s}" for s in set(setting_to_scug_id.values()).difference(set(scugs))], 1)


def one_of_these_scugs(scugs: list[str]) -> Simple:
    return Simple([f"Scug-{s}" for s in scugs], 1)


all_regions = [
    RegionData("Menu", "Menu"),
    RegionData("Early Passages", "(P1)"),
    RegionData("PPwS Passages", "(P2)"),
    RegionData("Late Passages", "(P3)"),
    RegionData("Food Quest", "(FQ)", generate.msc(True)),
    RegionData("Starting region", "START"),
    RegionData("Events", "(EV)"),

    RegionData("Outskirts", "SU"),
    RegionData("Industrial Complex", "HI"),
    RegionData("Drainage System", "DS", generate.blacklist_scugs(["Saint"])),
    RegionData("Garbage Wastes", "GW"),
    RegionData("Shoreline", "SL", generate.blacklist_scugs(["Artificer", "Spear"])),
    RegionData("Shoreline above Moon", "SL^", generate.blacklist_scugs(["Artificer", "Spear"])),
    RegionData("Shaded Citadel", "SH", generate.blacklist_scugs(["Saint"])),
    RegionData("The Exterior", "UW", generate.blacklist_scugs(["Saint"])),
    RegionData("Five Pebbles", "SS", generate.blacklist_scugs(["Rivulet", "Saint"])),
    RegionData("Five Pebbles above puppet", "SS^", generate.blacklist_scugs(["Rivulet", "Saint"])),
    RegionData("Chimney Canopy", "CC"),
    RegionData("Sky Islands", "SI"),
    RegionData("Farm Arrays", "LF"),
    RegionData("Subterranean", "SB"),
    RegionData("Subterranean ravine", "SB^"),
    RegionData("Void Sea", "(Vo)"),

    RegionData("Outskirts filtration", "SU^", generate.whitelist_scugs(["Yellow", "White", "Gourmand"], True)),
    RegionData("Pipeyard", "VS", generate.msc(True)),
    RegionData("Submerged Superstructure", "MS", generate.blacklist_scugs(["Artificer"], True)),
    RegionData("Bitter Aerie", "MS^", generate.whitelist_scugs(["Rivlet"], True)),
    RegionData("Outer Expanse", "OE", generate.whitelist_scugs(["Yellow", "White", "Gourmand"], True)),
    RegionData("Outer Expanse filtration", "OE^", generate.whitelist_scugs(["Yellow", "White", "Gourmand"], True)),
    RegionData("Metropolis", "LC", generate.whitelist_scugs(["Artificer"], True)),
    RegionData("Looks to the Moon", "DM", generate.whitelist_scugs(["Spear"], True)),
    RegionData("The Rot", "RM", generate.whitelist_scugs(["Rivulet"], True)),
    RegionData("Undergrowth", "UG", generate.whitelist_scugs(["Saint"], True)),
    RegionData("Silent Construct", "CL", generate.whitelist_scugs(["Saint"], True)),
    RegionData("Waterfront Facility", "LM", generate.whitelist_scugs(["Artificer", "Spear"], True)),
    RegionData("Eastern Precipice", "LM^", generate.whitelist_scugs(["Spear"], True)),
    RegionData("Rubicon", "HR", generate.whitelist_scugs(["Saint"], True)),
]


all_connections = [
    ConnectionData("Menu", "Early Passages"),
    ConnectionData("Early Passages", "Late Passages", Simple("Passage-Survivor", locations=True)),
    ConnectionData("Late Passages", "PPwS Passages"),  # default connect PPwS to late to require survivor
    ConnectionData("Menu", "Food Quest", Simple("MSC")),
    ConnectionData("Menu", "Starting region"),
    ConnectionData("Menu", "Events"),

    ConnectionData("Outskirts filtration", "Outskirts"),
    Gate("Outskirts", "Industrial Complex", 3, "SU_HI"),
    Gate("Outskirts", "Drainage System", 4, "SU_DS", any_scug_except(["Saint"])),
    Gate("Outskirts", "Undergrowth", 4, "SU_DS", one_of_these_scugs(["Saint"])),
    Gate("Outskirts", "Farm Arrays", 5, "LF_SU"),

    Gate("Industrial Complex", "Outskirts", 2, "SU_HI"),
    Gate("Industrial Complex", "Garbage Wastes", 2, "HI_GW"),
    Gate("Industrial Complex", "Chimney Canopy", 3, "HI_CC"),
    Gate("Industrial Complex", "Shaded Citadel", 5, "HI_SH", Simple(["The Glow", "Option-Glow"], 1)),
    Gate("Industrial Complex", "Pipeyard", 4, "HI_VS", Simple("MSC")),
    Gate("Industrial Complex", "Silent Construct", 4, "HI_VS", one_of_these_scugs(["Saint"])),

    Gate("Garbage Wastes", "Drainage System", 3, "DS_GW"),
    Gate("Garbage Wastes", "Industrial Complex", 2, "HI_GW"),
    Gate("Garbage Wastes", "Shoreline", 3, "GW_SL", any_scug_except(["Artificer", "Spear"])),
    Gate("Garbage Wastes", "Shaded Citadel", 4, "GW_SH", AllOf(Simple("MSC"), Simple(["The Glow", "Option-Glow"], 1))),
    Gate("Garbage Wastes", "Waterfront Facility", 3, "GW_SL", one_of_these_scugs(["Artificer", "Spear"])),
    Gate("Garbage Wastes", "Silent Construct", 4, "GW_SH", one_of_these_scugs(["Saint"])),
    Gate("Garbage Wastes", "Undergrowth", 3, "DS_GW", one_of_these_scugs(["Saint"])),

    Gate("Drainage System", "Outskirts", 2, "SU_DS"),
    Gate("Drainage System", "Garbage Wastes", 1, "DS_GW"),
    Gate("Drainage System", "Subterranean", 4, "DS_SB"),
    Gate("Drainage System", "Chimney Canopy", 5, "DS_CC", Simple("MSC")),

    Gate("Shoreline", "Garbage Wastes", 2, "GW_SL"),
    Gate("Shoreline", "Shaded Citadel", 2, "SH_SL",
         AllOf(any_scug_except(["Saint"]), Simple(["The Glow", "Option-Glow"], 1))),
    Gate("Shoreline", "Subterranean", 5, "SB_SL"),
    Gate("Shoreline", "Pipeyard", 3, "SL_VS", Simple("MSC")),
    Gate("Shoreline", "Submerged Superstructure", 5, "SL_MS", Simple("MSC")),
    # Gate("Shoreline", "Bitter Aerie", 6, "MS_SL",  Simple("MSC")),
    Gate("Shoreline", "Silent Construct", 5, "SH_SL", one_of_these_scugs(["Saint"])),
    ConnectionData("Shoreline above Moon", "Shoreline"),

    Gate("Shaded Citadel", "Industrial Complex", 1, "HI_SH"),
    Gate("Shaded Citadel", "Shoreline", 3, "SH_SL", any_scug_except(["Saint"])),
    Gate("Shaded Citadel", "The Exterior", 1, "SH_UW"),
    Gate("Shaded Citadel", "Garbage Wastes", 2, "GW_SH", Simple("MSC")),
    Gate("Shaded Citadel", "Waterfront Facility", 3, "SH_SL", one_of_these_scugs(["Artificer", "Spear"])),

    Gate("The Exterior", "Chimney Canopy", 1, "CC_UW"),
    Gate("The Exterior", "Shaded Citadel", 1, "SH_UW", Simple(["The Glow", "Option-Glow"], 1)),
    Gate("The Exterior", "Five Pebbles above puppet", 1, "SS_UW"),
    Gate("The Exterior", "Five Pebbles", 5, "UW_SS"),
    Gate("The Exterior", "Waterfront Facility", 3, "UW_SL", one_of_these_scugs(["Artificer", "Spear"])),
    Gate("The Exterior", "Metropolis", 5, "UW_LC", Simple(["Scug-Artificer", "The Mark", "IdDrone"])),
    Gate("The Exterior", "The Rot", 1, "SS_UW", one_of_these_scugs(["Rivulet"])),
    Gate("The Exterior", "The Rot", 5, "UW_SS", one_of_these_scugs(["Rivulet"])),

    Gate("Chimney Canopy", "Industrial Complex", 3, "HI_CC"),
    Gate("Chimney Canopy", "Sky Islands", 2, "SI_CC"),
    Gate("Chimney Canopy", "The Exterior", 4, "CC_UW"),
    Gate("Chimney Canopy", "Drainage System", 3, "DS_CC", Simple("MSC")),
    Gate("Chimney Canopy", "Undergrowth", 3, "DS_CC", one_of_these_scugs(["Saint"])),

    Gate("Sky Islands", "Chimney Canopy", 3, "SI_CC"),
    Gate("Sky Islands", "Farm Arrays", 3, "SI_LF"),
    Gate("Sky Islands", "Pipeyard", 3, "SI_VS", Simple("MSC")),

    Gate("Farm Arrays", "Outskirts", 2, "LF_SU"),
    Gate("Farm Arrays", "Sky Islands", 3, "SI_LF"),
    Gate("Farm Arrays", "Subterranean ravine", 4, "LF_SB"),

    ConnectionData("Subterranean ravine", "Subterranean"),
    Gate("Subterranean", "Drainage System", 1, "DS_SB"),
    Gate("Subterranean", "Shoreline", 2, "SB_SL"),
    Gate("Subterranean", "Pipeyard", 3, "SB_VS", Simple("MSC")),
    Gate("Subterranean", "Outer Expanse", 1, "SB_OE",
         Compound(2, Simple("MSC"), one_of_these_scugs(["Yellow", "White", "Gourmand"]))),
    Gate("Subterranean", "Waterfront Facility", 2, "SB_SL", one_of_these_scugs(["Artificer", "Rivulet"])),
    Gate("Subterranean", "Undergrowth", 1, "DS_SB", one_of_these_scugs(["Saint"])),
    # Gate("Subterranean", "Rubicon", 10, "DS_SB", one_of_these_scugs(["Saint"])),

    ConnectionData("Subterranean", "Void Sea", AllOf(Simple("Karma", 8), any_scug_except(["Saint"]))),

    ################################################################
    # DOWNPOUR - GENERAL

    Gate("Pipeyard", "Industrial Complex", 2, "HI_VS", Simple("MSC")),
    Gate("Pipeyard", "Shoreline", 3, "SL_VS", Simple("MSC")),
    Gate("Pipeyard", "Subterranean", 5, "SB_VS", Simple("MSC")),
    Gate("Pipeyard", "Sky Islands", 4, "SI_VS", Simple("MSC")),
    Gate("Pipeyard", "Waterfront Facility", 3, "SL_VS", one_of_these_scugs(["Artificer", "Rivulet"])),

    Gate("Five Pebbles", "The Exterior", 1, "UW_SS"),
    Gate("Five Pebbles above puppet", "The Exterior", 1, "SS_UW"),
    ConnectionData("Five Pebbles", "Five Pebbles above puppet"),

    ################################################################
    # DOWNPOUR - GOURMAND
    Gate("Outer Expanse", "Subterranean", 5, "SB_OE",  Simple("MSC")),
    ConnectionData("Outer Expanse", "Outer Expanse filtration"),
    Gate("Outer Expanse filtration", "Outskirts filtration", 1, "OE_SU",  Simple("MSC")),

    ################################################################
    # DOWNPOUR - ARTIFICER
    Gate("Waterfront Facility", "Garbage Wastes", 2, "GW_SL", Simple("MSC")),
    Gate("Waterfront Facility", "Pipeyard", 3, "GW_SL", Simple("MSC")),
    Gate("Waterfront Facility", "Subterranean", 5, "SB_SL", Simple("MSC")),
    Gate("Waterfront Facility", "The Exterior", 5, "UW_SL", Simple("MSC")),
    Gate("Waterfront Facility", "Shaded Citadel", 2, "SH_SL",
         AllOf(Simple("MSC"), Simple(["The Glow", "Option-Glow"], 1))),

    Gate("Metropolis", "The Exterior", 5, "UW_LC", Simple("MSC")),

    ################################################################
    # DOWNPOUR - RIVULET
    Gate("Bitter Aerie", "Shoreline above Moon", 5, "SL_MS", Simple("MSC")),
    Gate("Shoreline above Moon", "Bitter Aerie", 6, "SL_MS", Simple("MSC")),
    Gate("Submerged Superstructure", "Shoreline", 1, "MS_SL", Simple("MSC")),

    Gate("The Rot", "The Exterior", 1, "UW_SS", Simple("MSC")),
    Gate("The Rot", "The Exterior", 1, "SS_UW", Simple("MSC")),

    ################################################################
    # DOWNPOUR - SPEARMASTER
    Gate("Eastern Precipice", "Looks to the Moon", 5, "SL_DM", Simple(["MSC", "Scug-Spear"])),
    Gate("Waterfront Facility", "Looks to the Moon", 1, "DM_SL", Simple(["MSC", "Scug-Spear"])),

    Gate("Looks to the Moon", "Eastern Precipice", 1, "SL_DM", Simple("MSC")),
    Gate("Looks to the Moon", "Waterfront Facility", 1, "DM_SL", Simple("MSC")),
    ConnectionData("Waterfront Facility", "Eastern Precipice", Simple(["MSC", "Scug-Spear"])),
    ConnectionData("Eastern Precipice", "Waterfront Facility", Simple(["MSC", "Scug-Spear"])),

    ################################################################
    # DOWNPOUR - SAINT
    Gate("Undergrowth", "Outskirts", 2, "SU_DS", Simple("MSC")),
    Gate("Undergrowth", "Chimney Canopy", 5, "DS_CC", Simple("MSC")),
    Gate("Undergrowth", "Garbage Wastes", 1, "DS_GW", Simple("MSC")),
    Gate("Undergrowth", "Subterranean", 4, "DS_SB", Simple("MSC")),

    Gate("Silent Construct", "Industrial Complex", 1, "HI_SH", Simple("MSC")),
    Gate("Silent Construct", "Garbage Wastes", 2, "GW_SH", Simple("MSC")),
    Gate("Silent Construct", "Shoreline", 1, "SL_CL", Simple("MSC")),

    ConnectionData("Subterranean", "Rubicon", AllOf(Simple(["MSC", "Scug-Saint"]), Simple("Karma", 8))),
    ConnectionData("Rubicon", "Void Sea", AllOf(Simple("Karma", 8), one_of_these_scugs(["Saint"]))),
]

all_gate_short_names = set(item.gate_name for item in all_connections if type(item) == Gate)
