"""Hardcoded exceptions to the automatically extracted data."""


bitter_aerie_other_rooms = [
    "MS_COMMS", "MS_S07", "GATE_SL_MS", "MS_WILLSNAGGING", "MS_S10", "MS_JTRAP", "MS_PUMPS", "MS_SCAVTRADER", "MS_X02"
]


def bitter_aerie(data: dict) -> None:
    """Bitter Aerie rooms aren't blacklisted for non-Rivulets while the rest of MS is accessible."""
    for room, room_data in data["MSC"]["MS"].items():
        if "BITTER" in room or "AERIE" in room or "SEWER" in room or room in bitter_aerie_other_rooms:
            room_data["whitelist"] = {"Rivulet"}


def apply_hardcoded_exceptions(data: dict) -> None:
    bitter_aerie(data)
