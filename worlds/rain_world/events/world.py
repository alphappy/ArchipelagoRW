from .classes import StaticWorldEvent, StaticWorldEventDetached
from ..options import RainWorldOptions

from ..conditions.classes import Simple
from ..game_data.general import scugs_all, scugs_vanilla
from ..regions.classes import RainWorldRegion, room_to_region
from ..utils import (placed_object_effective_whitelist as POEW, creature_den_effective_whitelist as CDEW,
                     room_effective_whitelist as REW)


def generate_events_for_one_gamestate(options: RainWorldOptions, regions: list[RainWorldRegion])\
        -> list[StaticWorldEvent | StaticWorldEventDetached]:
    ret = []
    scugs = scugs_all if options.is_msc_enabled else scugs_vanilla
    detached: dict[str, list[str]] = {}

    for region in regions:
        if (rooms := region.rooms) and len(rooms) > 0:
            if region_data := options.data_block.get(region.code[:2], {}):
                for room in rooms:
                    if room_data := region_data.get(room, {}):
                        for obj_type, obj_data in room_data.get("objects", {}).items():
                            if options.starting_scug in POEW(room_data, obj_data, set(scugs)):
                                detached.setdefault(obj_type, []).append(room)

                        for crit_type, crit_data in room_data.get("spawners", {}).get("normal", {}).items():
                            if options.starting_scug in CDEW(room_data, crit_data, set(scugs)):
                                detached.setdefault(crit_type, []).append(room)

                        if room_tags := room_data.get("tags", []):
                            for tagname, eventname in (
                                    ("SWARMROOM", "Fly"), ("SCAVOUTPOST", "Toll"), ("SHELTER", "Shelter")
                            ):
                                if tagname in room_tags:
                                    whitelist = REW(room_data, set(scugs)).difference(room_data.get("broken", set()))
                                    if options.starting_scug in whitelist:
                                        detached.setdefault(eventname, []).append(room)

    # HARDCODE
    detached.setdefault("SSOracleSwarmer", []).extend(["SS_E07", "SL_AI", "RM_AI", "DM_AI", "LC_LAB01"])
    if options.starting_scug == "Inv":
        detached.setdefault("Yeek", ["GATE_HI_CC[CC]", "GATE_SI_CC[CC]", "GATE_CC_UW[CC]"])

    for event_type, event_rooms in detached.items():
        ret.append(StaticWorldEventDetached(event_type, event_rooms))

    if options.starting_scug in {"Yellow", "White", "Red", "Gourmand", "Rivulet", "Saint"}:
        ret.append(StaticWorldEvent("Meet LttM", f'Meet LttM', room_to_region["SL_AI"], Simple("The Mark")))

    return ret
