from .classes import LocationData, Echo
from ..conditions.classes import Simple, AnyOf
from ..conditions import generate

cond_normal = AnyOf(Simple("Karma", 4), Simple(["Scug-Artificer", "KarmaFlower"]), Simple("Scug-Saint"))
cond_no_saint = AnyOf(Simple("Karma", 4), Simple(["Scug-Artificer", "KarmaFlower"]))

locations: list[LocationData] = [
    Echo("CC", "CC_C12", 5070, "", cond_normal),
    Echo("SH", "SH_A08", 5071, "", cond_no_saint),
    Echo("LF", "LF_B01", 5072, "", cond_normal),
    Echo("UW", "UW_A14", 5073, "", cond_no_saint),
    Echo("SI", "SI_B11", 5074, "", cond_normal),
    Echo("SB", "SB_A10", 5075, "", cond_normal),
    Echo("LC", "LC_HIGHESTPOINT", 5076, "", Simple("Scug-Artificer")),
    Echo("UG", "UG_C02", 5077, "", Simple("Scug-Saint")),
    Echo("CL", "CL_D05", 5078, "", Simple("Scug-Saint")),
    Echo("SL", "SL_WALL06", 5079, "", Simple("Scug-Saint"), generate.whitelist_scugs(["Saint"], True)),
]
