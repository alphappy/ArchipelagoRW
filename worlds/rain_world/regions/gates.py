from BaseClasses import MultiWorld
from .classes import ConnectionData, RegionData
from ..options import RainWorldOptions
from ..conditions.classes import Condition, ConditionBlank, Simple, AllOf
from ..game_data.general import scugs_all


class GateData:
    def __init__(self, name: str, left: int, right: int,
                 left_extra: Condition = ConditionBlank, right_extra: Condition = ConditionBlank):
        self.name = name
        self.left = left
        self.right = right
        self.left_extra = left_extra
        self.right_extra = right_extra

    def make(self, player: int, multiworld: MultiWorld):
        for effective_name, scugs in self.effective_names().items():
            _, left_name, right_name = effective_name.split("_")

            left = multiworld.get_region(f'{self.name}[{left_name}]', player)
            right = multiworld.get_region(f'{self.name}[{right_name}]', player)
            left_condition = AllOf(
                self.left_extra,
                Simple("Karma", self.left - (1 if self.left < 6 else 2)),
                Simple([f"Scug-{s}" for s in scugs], 1),
                Simple(self.name)
            )
            right_condition = AllOf(
                self.right_extra,
                Simple("Karma", self.right - (1 if self.right < 6 else 2)),
                Simple([f"Scug-{s}" for s in scugs], 1),
                Simple(self.name)
            )

            if left.populate and right.populate:
                left.connect(right, rule=left_condition.check(player))
                right.connect(left, rule=right_condition.check(player))

    def effective_names(self) -> dict[str, set[str]]:
        ret = {self.name: set(scugs_all)}

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
    GateData("GATE_DS_SB", 4, 1),
    GateData("GATE_GW_SL", 3, 2),
    GateData("GATE_HI_CC", 3, 3),
    GateData("GATE_HI_GW", 2, 2),
    GateData("GATE_HI_SH", 5, 1),
    GateData("GATE_LF_SB", 4, 5),
    GateData("GATE_SB_SL", 2, 5),
    GateData("GATE_SH_UW", 1, 1),
    GateData("GATE_SH_SL", 3, 2),
    GateData("GATE_SI_CC", 3, 2),
    GateData("GATE_SI_LF", 3, 3),
    GateData("GATE_SS_UW", 1, 1),
    GateData("GATE_UW_SS", 5, 1),
    GateData("GATE_SL_MS", 999, 5),
    GateData("GATE_MS_SL", 1, 5),
    GateData("GATE_SB_OE", 1, 5, right_extra=Simple(["Scug-White", "Scug-Yellow", "Scug-Gourmand"], 1)),
    GateData("GATE_UW_LC", -1, 5, left_extra=Simple(["The Mark", "IdDrone", "Scug-Artificer"])),
    GateData("GATE_OE_SU", 1, 5),
    GateData("GATE_SL_DM", 5, 1),
    GateData("GATE_UW_SL", 1, 1),
    GateData("GATE_GW_SH", 4, 2),
    GateData("GATE_DS_CC", 5, 3),
    GateData("GATE_SL_CL", 5, 1),
    GateData("GATE_HI_VS", 4, 2),
    GateData("GATE_SL_VS", 3, 3),
    GateData("GATE_SB_VS", 3, 5),
    GateData("GATE_SI_VS", 3, 4),
    GateData("GATE_DM_SL", 1, 1),
]


def generate(options: RainWorldOptions) -> list[GateData]:
    return gates
