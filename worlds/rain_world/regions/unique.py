"""Unique connections between rooms."""
from ..options import RainWorldOptions
from ..conditions.classes import Simple
from .classes import ConnectionData


def generate(options: RainWorldOptions) -> list[ConnectionData]:
    if not options.msc_enabled:
        return []

    return [
        ConnectionData("MS_HEART", "MS_BITTERSTART", Simple(["Scug-Rivulet", "Object-EnergyCell"])),
        ConnectionData("OE_CAVE03", "OE_PUMP01"),
        ConnectionData("SB_E05SAINT", "HR_C01", Simple(["Scug-Saint"]))
    ]
