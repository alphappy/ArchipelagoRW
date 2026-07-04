from .classes import RegionData, ConnectionData
from ..locations.passages import generate_cond_survivor
from ..options import RainWorldOptions


def generate(options: RainWorldOptions):
    ret = [
        RegionData("Menu"),
        RegionData("Events"),
        RegionData("Early Passages"),
        RegionData("PPwS Passages"),
        RegionData("Late Passages"),
        RegionData("Food Quest",
                   options.msc_enabled and (options.checks_foodquest.value > 0 or options.starting_scug == "Gourmand")),

        ConnectionData("Menu", "Events", "Unique event checks"),
        ConnectionData("Menu", "Early Passages", "Early Passages"),
        ConnectionData("Early Passages", "Late Passages", "Late Passages",
                       generate_cond_survivor(options)),
        ConnectionData("Late Passages", "PPwS Passages", "PPwS Passages"),
        ConnectionData("Menu", "Food Quest", "Food Quest"),
    ]

    if options.passage_progress_without_survivor in ("enabled", "bypassed"):
        ret.append(ConnectionData("Menu", "PPwS Passages", "Passage progress without Survivor"))
    if options.passage_progress_without_survivor == "bypassed":
        ret.append(ConnectionData("Menu", "Late Passages", "Bypass Survivor requirement"))

    return ret



