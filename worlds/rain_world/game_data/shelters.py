from ..options import RainWorldOptions
from .general import alternate_regions, story_regions_vanilla

all_shelters = {
    'CC': ['CC_S04', 'CC_S05', 'CC_S01', 'CC_S03', 'CC_S06', 'CC_S07'],
    'CL': ['CL_S03', 'CL_S12', 'CL_S01', 'CL_S11', 'CL_S10', 'CL_S20', 'CL_S15', 'CL_S21', 'CL_LCS2', 'CL_S05', 'CL_S08', 'CL_S14', 'CL_S13', 'CL_S02'],
    'DM': ['DM_S01', 'DM_S04', 'DM_S03', 'DM_S05', 'DM_STOP', 'DM_S10', 'DM_S06', 'DM_LAB5', 'DM_S02', 'DM_S14', 'DM_S11', 'DM_S13'],
    'DS': ['DS_S03', 'DS_S01R', 'DS_S04', 'DS_S02L'],
    'GW': ['GW_S05', 'GW_S04', 'GW_S03', 'GW_S02', 'GW_S07', 'GW_S01', 'GW_S06', 'GW_S08', 'GW_S09'],
    'HI': ['HI_S06', 'HI_S03', 'HI_S01', 'HI_S02', 'HI_S05', 'HI_S04'],
    'HR': ['HR_S02', 'HR_S1R', 'HR_SHR', 'HR_S11', 'HR_S04', 'HR_S06', 'HR_S12', 'HR_S05', 'HR_S03', 'HR_S01', 'HR_S10'],
    'LC': ['LC_SHELTER_ABOVE', 'LC_A05', 'LC_SROOFS', 'LC_S03', 'LC_S01', 'LC_S06', 'LC_SHELTERTRAIN1', 'LC_S05', 'LC_S04'],
    'LF': ['LF_S04', 'LF_S02', 'LF_S06', 'LF_S01', 'LF_S07', 'LF_S05', 'LF_S03'],
    'LM': ['LM_S15', 'LM_S02', 'LM_S07', 'LM_S05', 'LM_S09', 'LM_S03', 'LM_S04', 'LM_S11', 'LM_S13', 'LM_S06'],
    'MS': ['MS_S01', 'MS_S04', 'MS_S05', 'MS_S03', 'MS_S06', 'MS_S09', 'MS_LAB5', 'MS_S07', 'MS_BITTERSHELTER', 'MS_S10'],
    'OE': ['OE_S01', 'OE_S04', 'OE_EXSHELTER', 'OE_MIDSHELTER', 'OE_S06', 'OE_SFINAL', 'OE_S03'],
    'RM': ['RM_S04', 'RM_S05', 'RM_S02', 'RM_S01', 'RM_S03', 'RM_LCS2', 'RM_LCS1', 'RM_SDEAD', 'RM_SFINAL'],
    'SB': ['SB_S06', 'SB_S07', 'SB_S03', 'SB_S04', 'SB_S05', 'SB_S02', 'SB_S01', 'SB_S10', 'SB_S09'],
    'SH': ['SH_S03', 'SH_S05', 'SH_S04', 'SH_S10', 'SH_S01', 'SH_S06', 'SH_S07', 'SH_S02', 'SH_S08', 'SH_S09', 'SH_S11'],
    'SI': ['SI_S03', 'SI_S04', 'SI_S05', 'SI_S06'],
    'SL': ['SL_SCRUSHED', 'SL_S02', 'SL_S13', 'SL_S07', 'SL_S05', 'SL_S10', 'SL_S06', 'SL_S09', 'SL_S03', 'SL_S08', 'SL_S04', 'SL_S11', 'SL_S15', 'SL_STOP'],
    'SS': ['SS_S04', 'SS_S05', 'SS_S02', 'SS_S01', 'SS_S03'],
    'SU': ['SU_S04', 'SU_S01', 'SU_S03', 'SU_S05'],
    'UG': ['UG_S03', 'UG_S01R', 'UG_S04', 'UG_S02L'],
    'UW': ['UW_S03', 'UW_S04', 'UW_S01', 'UW_S02', 'UW_S07', 'UW_S06', 'UW_S05'],
    'VS': ['VS_S04', 'VS_S01', 'VS_S20', 'VS_S09', 'VS_S05', 'VS_S07', 'VS_S02', 'VS_S06', 'VS_S08', 'VS_S03']
}

start_shelters = {
    'CC': ['CC_S04', 'CC_S01', 'CC_S03'],
    'CL': ['CL_S10', 'CL_S12', 'CL_LCS2', 'CL_S02', 'CL_S05', 'CL_S14'],
    'DM': ['DM_S01', 'DM_STOP', 'DM_S02', 'DM_S11', 'DM_S13'],
    'DS': ['DS_S01R', 'DS_S04', 'DS_S02L'],
    'GW': ['GW_S02', 'GW_S07', 'GW_S06'],
    'HI': ['HI_S06', 'HI_S01', 'HI_S02', 'HI_S05', 'HI_S04'],
    'LC': ['LC_SHELTER_ABOVE', 'LC_A05', 'LC_S03', 'LC_S01', 'LC_SHELTERTRAIN1', 'LC_S04'],
    'LF': ['LF_S02', 'LF_S01', 'LF_S07', 'LF_S05', 'LF_S03'],
    'LM': ['LM_S05', 'LM_S11', 'LM_S13', 'LM_S06'],
    'OE': ['OE_S01', 'OE_S04', 'OE_EXSHELTER', 'OE_S06'],
    'RM': ['RM_S01', 'RM_LCS2', 'RM_LCS1'],
    'SB': ['SB_S06', 'SB_S07', 'SB_S04', 'SB_S05', 'SB_S02'],
    'SH': ['SH_S04', 'SH_S10', 'SH_S02', 'SH_S08'],
    'SI': ['SI_S03', 'SI_S04', 'SI_S05'],
    'SL': ['SL_S07', 'SL_S05', 'SL_S10', 'SL_S09', 'SL_S03', 'SL_S08', 'SL_S04'],
    'SS': ['SS_S04', 'SS_S02', 'SS_S01'],
    'SU': ['SU_S04', 'SU_S01', 'SU_S03', 'SU_S05'],
    'UG': ['UG_S01R', 'UG_S04', 'UG_S02L'],
    'UW': ['UW_S04', 'UW_S01', 'UW_S02', 'UW_S07', 'UW_S06', 'UW_S05'],
    'VS': ['VS_S04', 'VS_S01', 'VS_S05', 'VS_S08']
}

ingame_capitalization = {
    "DS_S01R": "DS_S01r",
    "DS_S02L": "DS_S02l",
    "UG_S01R": "UG_S01r",
    "UG_S02L": "UG_S02l",
    "LC_SHELTER_ABOVE": "LC_shelter_above",
    "LC_SHELTERTRAIN1": "LC_ShelterTrain1",
}


def get_starts(options: RainWorldOptions) -> list[str]:
    code, name = options.random_starting_region.code, options.random_starting_region.name
    scug, scug_name = options.starting_scug, options.which_gamestate.scug_name

    if code == "!!!":
        if scug == "Spear":
            return ["GATE_OE_SU[SU]"]
        elif scug == "Gourmand":
            return ["SH_GOR02"]
        elif scug == "Artificer":
            return ["GW_A24"]
        elif scug == "Rivulet":
            return ["DS_RIVSTART"]
        elif scug == "Saint":
            return ["SI_SAINTINTRO"]
        elif scug == "Red":
            return ["LF_E04"]
        elif scug == "Inv":
            return ["SH_E03"]
        else:
            return ["SU_C04"]

    code = alternate_regions.get(code, {}).get(scug, code)

    if code is None:
        raise ValueError(f"Invalid YAML: {scug_name} cannot start in {name}")

    if code == "SH" and options.difficulty_glow:
        raise ValueError("Invalid YAML: Cannot start in Shaded Citadel with 'Glow required for dark places' enabled")

    if not options.msc_enabled and code not in story_regions_vanilla:
        raise ValueError(f"Invalid YAML: Cannot start in {name} with MSC disabled")

    if code == "LC":
        if scug != "Artificer":
            raise ValueError(f"Invalid YAML: {scug_name} cannot start in Metropolis")
        elif options.which_victory_condition == "alternate":
            raise ValueError(f"Invalid YAML: Artificer starting in Metropolis with alternate victory condition is moot")
    elif code == "OE":
        if scug not in ["White", "Yellow", "Gourmand"]:
            raise ValueError(f"Invalid YAML: {scug_name} cannot start in Outer Expanse")
        elif options.which_victory_condition == "alternate":
            raise ValueError(f"Invalid YAML: {scug_name} starting in {name} with alternate victory condition is moot")
    elif code == "DM" and scug != "Spear":
        raise ValueError(f"Invalid YAML: {scug_name} cannot start in Looks to the Moon")

    ret = list(start_shelters[code])

    # shelter does not exist in vanilla
    if code == "SU" and not options.msc_enabled:
        ret.remove("SU_S05")

    # going backwards through puppet room not in logic
    if code == "SS":
        ret.remove("SS_S04")

    if options.difficulty_glow:
        # dark shelters near filtration system
        if code == "SB":
            ret.remove("SB_S02")
            ret.remove("SB_S04")

    return ret
