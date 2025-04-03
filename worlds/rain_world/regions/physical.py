from ..game_data.general import region_code_to_name, scugs_all
from ..game_data import static_data
from ..conditions.classes import Simple, AllOf
from ..options import RainWorldOptions
from .classes import ConnectionData, PhysicalRegion


def _generate(options: RainWorldOptions) -> list[PhysicalRegion | ConnectionData]:
    ret = []
    for region, region_data in static_data["1.10.1"]["MSC_Watcher"].items():
        rooms = set(region_data.keys())

        match region:
            case "SU":
                # Not in logic (except for Saint) to go backwards through the tutorial/filtration area.
                filt = {r for r in rooms if "CAVE" in r or "PUMP" in r
                        or r in ("SU_VR1", "SU_PS1", "SU_C04", "SU_A41", "SU_A42", "SU_A43", "SU_A44", "SU_S05",
                                 "SU_INTRO01", "SU_X02", "SU_S10", "GATE_OE_SU[SU]")}
                ret += [
                    PhysicalRegion("Outskirts", "SU", rooms.difference(filt)),
                    PhysicalRegion("Outskirts filtration", "SU^", filt),
                    ConnectionData("Outskirts filtration", "Outskirts", "Exit Survivor tutorial area"),
                    ConnectionData("Outskirts", "Outskirts filtration", "Return to Survivor tutorial area",
                                   Simple("Scug-Saint")),
                ]

            case "MS":
                # Not in logic to access Bitter Aerie except as Rivulet.
                bitter = {name for name in rooms if "BITTER" in name or "SEWER" in name or "AERIE" in name
                          or name in ("MS_WILLSNAGGING01", "MS_S07", "MS_PUMPS", "MS_SCAVTRADER", "MS_JTRAP",
                                      "MS_COMMS", "GATE_SL_MS[MS]")}
                ret += [
                    PhysicalRegion("Submerged Superstructure", "MS", rooms.difference(bitter)),
                    PhysicalRegion("Bitter Aerie", "MS^", bitter),
                    ConnectionData("Submerged Superstructure", "Bitter Aerie", "Rarefaction cell deposit cutscene",
                                   Simple(["Scug-Rivulet", "Rarefaction Cell"])),
                ]

            case "SB":
                # Not in logic (except for Saint) to go back up the SB ravine.
                ravine = {"SB_A10", "SB_F03", "SB_TOPSIDE", "SB_S09", "GATE_LF_SB[SB]"}
                filt = {"SB_C05", "SB_C06", "SB_S03", "SB_S04", "SB_D04", "SB_F02", "SB_I01", "SB_E07", "SB_C10",
                        "SB_B04", "SB_S10", "SB_G04", "GATE_SB_VS[SB]", "SB_F01", "SB_J03", "GATE_DS_SB[SB]", "SB_S02"}
                depths = {"SB_E05", "SB_A14", "SB_D02", "SB_E03", "SB_A07", "SB_A02", "SB_J04", "SB_A08", "SB_B03",
                          "SB_D05", "SB_A06", "SB_A05", "SB_D03", "SB_D07", "SB_D01", "SB_C08", "SB_E01", "SB_E06",
                          "SB_C09", "SB_L01"}
                ret += [
                    PhysicalRegion("Subterranean", "SB", rooms.difference(ravine.union(filt).union(depths))),
                    PhysicalRegion("Subterranean ravine", "SB^", ravine),
                    ConnectionData("Subterranean ravine", "Subterranean", "Down the ravine"),
                    ConnectionData("Subterranean", "Subterranean ravine", "Up the ravine",
                                   Simple("Scug-Saint")),

                    PhysicalRegion("Filtration System", "SB^2", filt),
                    ConnectionData("Subterranean", "Filtration System", "Enter Filtration System",
                                   Simple(["The Glow", "Option-Glow"], 1)),
                    ConnectionData("Filtration System", "Subterranean", "Exit Filtration System"),

                    PhysicalRegion("Subterranean Depths", "SB^3", depths),
                    ConnectionData("Filtration System", "Subterranean Depths", "Enter Depths")
                ]

            case "SS":
                # Not in logic to go backwards through Five Pebbles puppet room.
                above = {"GATE_SS_UW[SS]", "SS_D08", "SS_S04", "SS_E08", "SS_D07", "SS_AI"}
                ret += [
                    PhysicalRegion("Five Pebbles", "SS", rooms.difference(above)),
                    PhysicalRegion("Five Pebbles above puppet", "SS^", above),
                    ConnectionData("Five Pebbles", "Five Pebbles above puppet", "Out the access shaft")
                ]

            case "VS":
                # Not in logic to go through Sump Tunnel as Artificer.
                sump = {"VS_A09", "VS_A10", "VS_B13", "VS_S06", "VS_B15", "VS_A11", "VS_B14", "VS_A12", "VS_A15",
                        "VS_B18", "VS_D05", "VS_C08", "VS_E01", "VS_B05", "VS_D02", "VS_S02", "GATE_SL_VS[VS]"}
                filt = {"VS_C10", "VS_C12", "VS_C11", "VS_E02", "VS_B06", "BS_S03", "VS_H01", "GATE_SB_VS[VS]",
                        "VS_S03"}
                ret += [
                    PhysicalRegion("Pipeyard", "VS", rooms.difference(sump.union(filt))),
                    PhysicalRegion("Sump Tunnel", "VS^", sump),
                    ConnectionData("Pipeyard", "Sump Tunnel", "Enter Sump Tunnel",
                                   Simple(list(set(scugs_all).difference({"Artificer"})), 1)),
                    ConnectionData("Sump Tunnel", "Pipeyard", "Exit Sump Tunnel",
                                   Simple(list(set(scugs_all).difference({"Artificer"})), 1)),
                    PhysicalRegion("Pipeyard filtration", "VS^2", filt),
                    ConnectionData("Pipeyard", "Pipeyard filtration", "Enter dark filtration area",
                                   Simple(["The Glow", "Option-Glow"], 1)),
                    ConnectionData("Pipeyard filtration", "Pipeyard", "Exit dark filtration area"),
                ]

            case "UW":
                west_underhang = {"UW_C04", "UW_D05", "UW_A04", "UW_C02", "UW_C02RIV", "UW_D05RIV", "UW_A04RIV"}
                east_underhang_and_leg = {
                    "UW_A05", "UW_C01", "UW_A03", "UW_A10", "UW_J01", "UW_I01", "UW_C08", "GATE_UW_SS", "UW_A11",
                    "UW_S02", "UW_A06", "UW_E04", "UW_A08", "UW_C03", "UW_D04", "UW_B01", "UW_D03", "UW_E03", "UW_A09",
                    "UW_S06", "UW_C06", "UW_E02", "UW_A07", "UW_D02", "UW_S05", "GATE_SH_UW"
                    "UW_A05RIV", "UW_C01RIV", "UW_A11RIV", "UW_J02RIV", "UW_A06RIV", "UW_E04RIV"
                }
                remainder = rooms.difference(west_underhang).difference(east_underhang_and_leg)

                ret += [
                    PhysicalRegion("The Exterior", "UW", remainder),
                    PhysicalRegion("Western Underhang", "UW^", west_underhang),
                    PhysicalRegion("Eastern Underhang + The Leg", "UW^2", east_underhang_and_leg),

                    # Going into Underhang from the west requires a grapple worm.
                    # In Vanilla Survivor and Monk worldstates, there isn't one in D06 (but there is in CC).
                    ConnectionData("The Exterior", "Western Underhang", "UW_D06 to UW_C04", Simple("TubeWorm")),
                    ConnectionData("Western Underhang", "The Exterior", "UW_C04 to UW_D06"),
                    ConnectionData("Western Underhang", "Eastern Underhang + The Leg", "UW_C02 to UW_A05"),
                ]

                # Westward through Underhang is not terribly reasonable for Rivulet.
                if options.starting_scug != "Rivulet":
                    ret += [ConnectionData("Eastern Underhang + The Leg", "Western Underhang", "UW_A05 to UW_C02")]

            case "SL":
                broken_precipice = {"GATE_UW_SL[SL]", "SL_BRIDGEEND", "SL_S13", "SL_EDGE01", "SL_EDGE02", "SL_BRIDGE01"}
                above_moon = {
                    "SL_MOONTOP", "SL_ROOF04", "SL_ACCSHAFT", "SL_ROOF03", "GATE_SL_MS[SL]", "SL_TEMPLE", "SL_STOP",
                    "SL_ROOF01", "SL_WALL06"
                }
                remainder = rooms.difference(broken_precipice).difference(above_moon)

                ret += [
                    PhysicalRegion("Shoreline", "SL", remainder),
                    PhysicalRegion("Broken Precipice", "SL^", broken_precipice),
                    PhysicalRegion("Shoreline above puppet", "SL^2", above_moon),

                    ConnectionData("Shoreline above puppet", "Shoreline", "Enter puppet room")
                ]

                if options.starting_scug == "Saint":
                    ret += [ConnectionData("Shoreline", "Shoreline above puppet", "Exit top of puppet room")]

            case _:
                ret.append(PhysicalRegion(region_code_to_name[region], region, rooms))

    ret.append(ConnectionData("Subterranean", "Rubicon", "Enter Rubicon",
                              AllOf(Simple("Karma", 8), Simple("Scug-Saint"))))

    return ret


def generate(options: RainWorldOptions):
    return _generate(options)
