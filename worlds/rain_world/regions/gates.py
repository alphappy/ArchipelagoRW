from BaseClasses import MultiWorld
from .classes import room_to_region
from ..options import RainWorldOptions
from ..conditions.classes import Condition, ConditionBlank, Simple, AllOf, AnyOf
from ..game_data.general import scugs_all, accessible_gates, region_code_to_name, direct_alternate_regions
from ..utils_ap import try_get_region


class GateData:
    def __init__(self, name: str, left: int, right: int, was_swapped: bool = False):
        self.name = name
        self.left = left
        self.right = right
        self.was_swapped = was_swapped

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        dlcstate = "MSC" if options.msc_enabled else "Vanilla"
        if self.name[5:] not in accessible_gates[dlcstate][options.starting_scug]:
            return

        for effective_name, scugs in self.effective_names(options).items():
            _, left_name, right_name = effective_name.split("_")

            left = try_get_region(multiworld, room_to_region[f'{self.name}[{left_name}]'], player)
            right = try_get_region(multiworld, room_to_region[f'{self.name}[{right_name}]'], player)

            if not left or not right:
                continue

            match options.which_gate_behavior:
                case "karma_only":
                    left_cost = Simple("Karma", self.left - (1 if self.left < 6 else 2))
                    right_cost = Simple("Karma", self.right - (1 if self.right < 6 else 2))
                case "key_only":
                    left_cost = Simple(self.item_name)
                    right_cost = Simple(self.item_name)
                case "key_and_karma":
                    left_cost = AllOf(Simple(self.item_name), Simple("Karma", self.left - (1 if self.left < 6 else 2)))
                    right_cost = AllOf(Simple(self.item_name), Simple("Karma", self.right - (1 if self.right < 6 else 2)))
                case "key_or_karma":
                    left_cost = AnyOf(Simple(self.item_name), Simple("Karma", self.left - (1 if self.left < 6 else 2)))
                    right_cost = AnyOf(Simple(self.item_name), Simple("Karma", self.right - (1 if self.right < 6 else 2)))
                case _:
                    raise ValueError(f"invalid setting: {options.which_gate_behavior=}")

            _l, _r = self.additional_conditions(options)
            left_condition = AllOf(_l, Simple([f"Scug-{s}" for s in scugs], 1), left_cost)
            right_condition = AllOf(_r, Simple([f"Scug-{s}" for s in scugs], 1), right_cost)

            if left.populate and right.populate:
                left.connect(
                    right, f"{'west' if self.was_swapped else 'east'} through {self.name}",
                    rule=left_condition.check(player)
                )
                right.connect(
                    left, f"{'east' if self.was_swapped else 'west'} through {self.name}",
                    rule=right_condition.check(player)
                )

    @property
    def item_name(self) -> str:
        return self.names[0]

    @property
    def names(self) -> list[str]:
        _, left_code, right_code = self.name.split("_")
        left_name, right_name = region_code_to_name[left_code], region_code_to_name[right_code]

        if self.name == "GATE_SS_UW": right_name = "The Wall"
        if self.name == "GATE_UW_SS": left_name = "Underhang"
        if self.name == "GATE_SL_MS": right_name = "Bitter Aerie"
        if self.name == "GATE_SL_DM": left_name = "The Precipice"
        if self.name == "GATE_DM_SL": left_name, right_name = "The Struts", "Waterfront Facility"

        ret = [f'Gate: {left_name} to {right_name}', f'Gate: {right_name} to {left_name}']

        for alt in direct_alternate_regions.get(left_code, []):
            left_alt = region_code_to_name[alt]
            ret += [f'Gate: {left_alt} to {right_name}', f'Gate: {right_name} to {left_alt}']

        for alt in direct_alternate_regions.get(right_code, []):
            right_alt = region_code_to_name[alt]
            ret += [f'Gate: {left_name} to {right_alt}', f'Gate: {right_alt} to {left_name}']

        return ret + [self.name]

    def is_accessible(self, options: RainWorldOptions):
        return self.name[5:] in accessible_gates[options.dlcstate][options.starting_scug]

    def additional_conditions(self, options: RainWorldOptions) -> tuple[Condition, Condition]:
        left, right, gg = [], [], self.name[5:]

        if options.difficulty_glow:
            if gg in ("HI_SH", "GW_SH", "DS_SB"):
                left.append("The Glow")
            elif gg in ("SH_UW", "SH_SL", "SB_VS"):
                right.append("The Glow")

        if gg == "SB_OE":
            if not options.msc_enabled or options.starting_scug not in ("White", "Yellow", "Gourmand"):
                left = ["Impossible"]
            if options.starting_scug == "Gourmand":
                left.append("The Mark")

        if gg == "UW_LC":
            if not (options.msc_enabled and options.starting_scug == "Artificer"):
                left = ["Impossible"]
            left += ["The Mark", "Citizen ID Drone"]

        if gg == "MS_SL" and options.starting_scug == "Rivulet" and options.difficulty_submerged:
            left.append("Disconnect_FP")

        return Simple(left), Simple(right)

    def effective_names(self, options: RainWorldOptions) -> dict[str, set[str]]:
        ret = {self.name: set(scugs_all)}

        if not options.msc_enabled:
            return ret

        if "DS" in self.name:
            ret[self.name.replace("DS", "UG")] = {"Saint"}
            ret[self.name].remove("Saint")

        if self.name in ["GATE_HI_SH", "GATE_GW_SH"]:
            ret[self.name.replace("SH", "CL")] = {"Saint"}
            ret[self.name].remove("Saint")

        if "SL" in self.name and "CL" not in self.name and "MS" not in self.name:
            ret[self.name.replace("SL", "LM")] = {"Artificer", "Spear"}
            # DM_SL and SL_DM don't have SL counterparts and so should be processed exclusively as DM_LM and LM_DM.
            if "DM" in self.name:
                del ret[self.name]
            else:
                ret[self.name].remove("Artificer")
                ret[self.name].remove("Spear")

        if "SS" in self.name:
            ret[self.name.replace("SS", "RM")] = {"Rivulet"}
            ret[self.name].remove("Rivulet")

        return ret


gates = [
    GateData("GATE_SU_DS", 4, 2),
    GateData("GATE_SU_HI", 3, 2),
    GateData("GATE_LF_SU", 2, 5),
    GateData("GATE_CC_UW", 4, 1),
    GateData("GATE_DS_GW", 1, 3),
    GateData("GATE_DS_SB", 4, 1, True),
    GateData("GATE_GW_SL", 3, 2),
    GateData("GATE_HI_CC", 3, 3, True),
    GateData("GATE_HI_GW", 2, 2),
    GateData("GATE_HI_SH", 5, 1),
    GateData("GATE_LF_SB", 4, 5, True),
    GateData("GATE_SB_SL", 2, 5),
    GateData("GATE_SH_UW", 1, 1),
    GateData("GATE_SH_SL", 3, 2),
    GateData("GATE_SI_CC", 3, 2),
    GateData("GATE_SI_LF", 3, 3),
    GateData("GATE_SS_UW", 1, 1),
    GateData("GATE_UW_SS", 5, 1),
    GateData("GATE_SL_MS", 999, 5),
    GateData("GATE_MS_SL", 1, 5, True),
    GateData("GATE_SB_OE", 1, 5, True),
    GateData("GATE_UW_LC", -1, 5),
    GateData("GATE_OE_SU", 1, 5),
    GateData("GATE_SL_DM", 5, 1),
    GateData("GATE_UW_SL", 1, 1),
    GateData("GATE_GW_SH", 4, 2),
    GateData("GATE_DS_CC", 5, 3),
    GateData("GATE_SL_CL", 5, 1),
    GateData("GATE_HI_VS", 4, 2),
    GateData("GATE_SL_VS", 3, 3),
    GateData("GATE_SB_VS", 3, 5),
    GateData("GATE_SI_VS", 3, 4, True),
    GateData("GATE_DM_SL", 1, 1),
]


def generate(_: RainWorldOptions) -> list[GateData]:
    return gates
