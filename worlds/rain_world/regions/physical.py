from ..game_data.general import region_code_to_name, scugs_all
from ..game_data import static_data
from ..conditions.classes import Simple, AnyOf, AllOf, ConditionBlank
from ..options import RainWorldOptions
from .classes import ConnectionData, PhysicalRegion


def _generate(options: RainWorldOptions) -> list[PhysicalRegion | ConnectionData]:
    ret = []
    for region, region_data in static_data["MSC_Watcher"].items():
        rooms = set(region_data.keys())

        match region:
            case "SU":
                # Not in logic (except for Saint) to go backwards through the tutorial/filtration area.
                tutorial = {"SU_C04", "SU_A41", "SU_A42", "SU_A44", "SU_A43"}
                spearspawn = {"GATE_OE_SU[SU]", "SU_INTRO01"}
                filt = {r for r in rooms if "CAVE" in r or "PUMP" in r or r in ("SU_VR1", "SU_PS1", "SU_S05", "SU_PMPSTATION01")}
                remainder = rooms.difference(filt).difference(tutorial).difference(spearspawn)

                ret += [
                    PhysicalRegion("Outskirts", "SU", remainder),
                    PhysicalRegion("Outskirts filtration", "SU^", filt),
                    PhysicalRegion("Survivor tutorial area", "SU^2", tutorial),
                    PhysicalRegion("Spearmaster spawn area", "SU^3", spearspawn),

                    ConnectionData("Survivor tutorial area", "Outskirts", "Eastward from SU_A43 to SU_A22"),

                    ConnectionData("Outskirts filtration", "Survivor tutorial area", "Eastward from SU_CAVE01 to SU_C04"),

                    ConnectionData("Spearmaster spawn area", "Outskirts filtration", "Upward from SU_INTRO01 to SU_PMPSTATION01"),
                ]

                if options.starting_scug in ("Saint", "Artificer") or "Explosive Jump Perk" in options.expedition_perks.value:
                    cond = Simple("Explosive Jump Perk") if "Explosive Jump Perk" in options.expedition_perks.value else ConditionBlank
                    ret += [
                        ConnectionData("Outskirts", "Survivor tutorial area", "Westward from SU_A22 to SU_A43", cond),
                        ConnectionData("Survivor tutorial area", "Outskirts filtration", "Westward from SU_C04 to SU_CAVE01", cond),
                    ]

            case "OE":
                filt = {r for r in rooms if "PUMP" in r or r in ("OE_S03", "GATE_OE_SU[OE]")}

                ret += [
                    PhysicalRegion("Outer Expanse", "OE", rooms.difference(filt)),
                    PhysicalRegion("Outer Expanse filtration", "OE^", filt),

                    ConnectionData("Outer Expanse", "Outer Expanse filtration", "Fall from OE_CAVE03 to OE_PUMP01")
                ]

            case "MS":
                # Not in logic to access Bitter Aerie except as Rivulet.
                bitter = {name for name in rooms if "BITTER" in name or "SEWER" in name or "AERIE" in name
                          or name in ("MS_WILLSNAGGING01", "MS_S07", "MS_PUMPS", "MS_SCAVTRADER", "MS_JTRAP",
                                      "MS_COMMS", "GATE_SL_MS[MS]", "MS_X02", "MS_S10")}
                ret += [
                    PhysicalRegion("Submerged Superstructure", "MS", rooms.difference(bitter)),
                    PhysicalRegion("Bitter Aerie", "MS^", bitter),
                ]

                if options.starting_scug == "Rivulet":
                    ret.append(ConnectionData("Submerged Superstructure", "Bitter Aerie",
                                              "Rarefaction cell deposit cutscene", Simple(["Rarefaction Cell"])))
                elif options.starting_scug == "Saint":
                    ret += [ConnectionData("Submerged Superstructure", "Bitter Aerie", "Enter Bitter Aerie"),
                            ConnectionData("Bitter Aerie", "Submerged Superstructure", "Leave Bitter Aerie")]


            case "SB":
                # Not in logic (except for Saint) to go back up the SB ravine.
                ravine = {"SB_A10", "SB_F03", "SB_TOPSIDE", "SB_S09", "GATE_LF_SB[SB]"}
                filt = {"SB_C05", "SB_C06", "SB_S03", "SB_S04", "SB_D04", "SB_F02", "SB_I01", "SB_E07", "SB_C10", "SB_S01",
                        "SB_B04", "SB_S10", "SB_G04", "GATE_SB_VS[SB]", "SB_F01", "SB_J03", "GATE_DS_SB[SB]", "SB_S02"}
                depths = {"SB_E05", "SB_A14", "SB_D02", "SB_E03", "SB_A07", "SB_A02", "SB_J04", "SB_A08", "SB_B03",
                          "SB_D05", "SB_A06", "SB_A05", "SB_D03", "SB_D07", "SB_D01", "SB_C08", "SB_E01", "SB_E06",
                          "SB_C09", "SB_L01"}
                ret += [
                    PhysicalRegion("Subterranean", "SB", rooms.difference(ravine.union(filt).union(depths))),
                    PhysicalRegion("Subterranean ravine", "SB^", ravine),
                    ConnectionData("Subterranean ravine", "Subterranean", "Down the ravine"),

                    PhysicalRegion("Filtration System", "SB^2", filt),
                    ConnectionData("Subterranean", "Filtration System", "Enter Filtration System",
                                   Simple("The Glow") if options.difficulty_glow else ConditionBlank),
                    ConnectionData("Filtration System", "Subterranean", "Exit Filtration System"),

                    PhysicalRegion("Subterranean Depths", "SB^3", depths),
                    ConnectionData("Filtration System", "Subterranean Depths", "Enter Depths")
                ]

                if options.starting_scug == "Saint":
                    ret.append(ConnectionData("Subterranean", "Subterranean ravine", "Up the ravine"))


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

                sump_cond = Simple("Aquatic Perk") if options.starting_scug == "Artificer" else ConditionBlank

                ret += [
                    PhysicalRegion("Pipeyard", "VS", rooms.difference(sump.union(filt))),
                    PhysicalRegion("Sump Tunnel", "VS^", sump),
                    ConnectionData("Pipeyard", "Sump Tunnel", "Enter Sump Tunnel", sump_cond),
                    ConnectionData("Sump Tunnel", "Pipeyard", "Exit Sump Tunnel", sump_cond),
                    PhysicalRegion("Pipeyard filtration", "VS^2", filt),
                    ConnectionData("Pipeyard", "Pipeyard filtration", "Enter dark filtration area",
                                   Simple("The Glow") if options.difficulty_glow else ConditionBlank),
                    ConnectionData("Pipeyard filtration", "Pipeyard", "Exit dark filtration area"),
                ]

            case "UW":
                west_underhang = {"UW_C04", "UW_D05", "UW_A04", "UW_C02", "UW_C02RIV", "UW_D05RIV", "UW_A04RIV"}
                east_underhang_and_leg = {
                    "UW_A05", "UW_C01", "UW_A03", "UW_A10", "UW_J01", "UW_I01", "UW_C08", "GATE_UW_SS[UW]", "UW_A11",
                    "UW_S02", "UW_A06", "UW_E04", "UW_A08", "UW_C03", "UW_D04", "UW_B01", "UW_S07", "UW_PREGATE",
                    "GATE_UW_SL[UW]", "UW_D03", "UW_E03", "UW_A09", "UW_S06", "UW_C06", "UW_E02", "UW_A07", "UW_D02",
                    "UW_S05", "GATE_SH_UW[UW]",
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
                near_submerged_gate = {"SL_C15", "SL_WALL02", "SL_WALL05", "SL_S15", "GATE_MS_SL[SL]"}
                remainder = rooms.difference(broken_precipice).difference(above_moon).difference(near_submerged_gate)

                ret += [
                    PhysicalRegion("Shoreline", "SL", remainder),
                    PhysicalRegion("Broken Precipice", "SL^", broken_precipice),
                    PhysicalRegion("Shoreline above puppet", "SL^2", above_moon),
                    PhysicalRegion("Shoreline near gate to Submerged", "SL^3", near_submerged_gate),

                    ConnectionData("Shoreline above puppet", "Shoreline", "Enter puppet room"),
                    ConnectionData("Shoreline near gate to Submerged", "Shoreline", "Leaving Submerged")
                ]

                if options.starting_scug == "Saint":
                    ret += [ConnectionData("Shoreline", "Shoreline above puppet", "Exit top of puppet room")]

                # If Submerged has no checks, swimming down towards the gate is not in logic.
                if options.submerged_should_populate:
                    if options.difficulty_submerged >= 1 and options.starting_scug != "Rivulet" and "Aquatic Perk" in options.expedition_perks.value:
                        ret += [ConnectionData("Shoreline", "Shoreline near gate to Submerged",
                                               "Entering towards Submerged", Simple("Aquatic Perk"))]
                    else:
                        ret += [ConnectionData("Shoreline", "Shoreline near gate to Submerged",
                                               "Entering towards Submerged")]

            case "WARA":
                western = {f"WARA_{r}" for r in {"E08", "P04", "P03", "P08", "P05", "P02", "S23", "P19"}}
                remainder = rooms.difference(western)

                ret += [
                    PhysicalRegion("Shattered Terrace", "WARA", remainder),
                    PhysicalRegion("Western Shattered Terrace", "WARA^1", western),
                    # Rightwards through WARA_P20 just needs the minimum amount of float
                    ConnectionData("Western Shattered Terrace", "Shattered Terrace", "WARA_P20 to WARA_P01",
                                   Simple("Ripple", 4)),
                    # Leftwards can be jumped easily
                    ConnectionData("Shattered Terrace", "Western Shattered Terrace", "WARA_P20 to WARA_P19"),
                ]

            case "WMPA":
                western = {f"WMPA_{r}" for r in {"A09", "A06", "A04", "A02", "A05", "S01", "A03", "A01", "A07", "A08"}}
                eastern = rooms.difference(western)

                ret += [
                    PhysicalRegion("Migration Path", "WMPA", eastern),
                    PhysicalRegion("Western Migration Path", "WMPA^1", western),
                    # Leftwards through the top of WMPA_B01 needs maximum float ability to cross
                    ConnectionData("Migration Path", "Western Migration Path", "WMPA_B01 to WMPA_A08",
                                   Simple("Ripple", 8)),
                    # Rightwards is just a drop-down
                    ConnectionData("Western Migration Path", "Migration Path", "WMPA_A08 to WMPA_B01"),
                ]

            # Yes I know it's kinda cursed
            case "WORA":
                # Path from WORA_START up through the throne
                western = {f"WORA_{r}" for r in {
                    "AI", "THRONE02", "THRONES01", "THRONE06", "THRONE08", "THRONE04", "THRONE12", "THRONE11",
                    "THRONE03", "THRONE1", "S03", "DESERT10", "DESERT9", "DESERT8", "DESERT7", "DESERT6", "DESERT3X",
                    "DESERT11", "START"
                }}
                # Egg
                egg = {f"WORA_{r}" for r in {"STARCATCHER08", "STARCATCHER06", "STARCATCHER07", "EGG03", "EGG04", "EGG02x", "EGG"}}
                # Throne rooms locked by ripple requirements
                ripple_locked_3 = {"WORA_THRONE10"}
                ripple_locked_5 = {"WORA_THRONE05"}
                ripple_locked_7 = {"WORA_THRONE07"}
                ripple_locked_9 = {"WORA_THRONE09", "WORA_THRONES01"}
                remainder = rooms.difference({*western, *egg, *ripple_locked_3, *ripple_locked_5, *ripple_locked_7, *ripple_locked_9})

                ret += [
                    PhysicalRegion("Outer Rim", "WORA", remainder),
                    PhysicalRegion("Western Outer Rim", "WORA^1", western),
                    PhysicalRegion("Eastern Outer Rim", "WORA^2", egg),
                    PhysicalRegion("The Throne 1", "WORA^3", ripple_locked_3),
                    PhysicalRegion("The Throne 2", "WORA^4", ripple_locked_5),
                    PhysicalRegion("The Throne 3", "WORA^5", ripple_locked_7),
                    PhysicalRegion("The Throne 4", "WORA^6", ripple_locked_9),
                    # Can't climb up into the rest of WORA from the initial spawn point (at WORA_DESERT8)
                    ConnectionData("Outer Rim", "Western Outer Rim", "WORA_DESERT5 TO WORA_DESERT8"),
                    # Kinda jank, but this handles the logic of warp target into WORA changing as you open more throne rooms
                    # Second encounter requires Ripple 5, at which point warps will go to central WORA
                    # TODO: If warps are changed to be able to send player to WORA more often, this will only need first encounter
                    ConnectionData("Western Outer Rim", "Outer Rim", "Prince encounter opens middle WORA",
                                   Simple("Ripple", 4)),
                    # Crossing the bridge doesn't technically require float, but reaching WORA_EGG does
                    # Simpler and more convenient to just gate all the nearby checks
                    ConnectionData("Outer Rim", "Eastern Outer Rim", "WORA_COLBRIDGE to WORA_STARCATCHER08",
                                   Simple("Ripple", 4)),
                    ConnectionData("Eastern Outer Rim", "Outer Rim", "WORA_COLBRIDGE to WORA_STARCATCHER09",
                                   Simple("Ripple", 4)),
                    # Ripple requirements to enter throne rooms
                    ConnectionData("Western Outer Rim", "The Throne 1", "Throne to WORA_THRONE10",
                                   Simple("Ripple", 2)),
                    ConnectionData("Western Outer Rim", "The Throne 2", "Throne to WORA_THRONE05",
                                   Simple("Ripple", 4)),
                    ConnectionData("Western Outer Rim", "The Throne 3", "Throne to WORA_THRONE07",
                                   Simple("Ripple", 6)),
                    ConnectionData("Western Outer Rim", "The Throne 4", "Throne to WORA_THRONE09",
                                   Simple("Ripple", 8)),
                ]

            case _:
                ret.append(PhysicalRegion(region_code_to_name[region], region, rooms))

    if options.starting_scug == "Saint":
        ret.append(ConnectionData("Subterranean", "Rubicon", "Enter Rubicon", Simple("Karma", 8)))

    return ret


def generate(options: RainWorldOptions):
    return _generate(options)
