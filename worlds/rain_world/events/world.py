from .classes import StaticWorldEvent
from ..conditions import GameStateFlag
from ..options import RainWorldOptions

from ..conditions.classes import Simple
from ..game_data.general import scugs_all, scugs_vanilla
from ..regions.classes import RainWorldRegion, room_to_region
from ..utils import (placed_object_effective_whitelist as POEW, creature_den_effective_whitelist as CDEW,
                     room_effective_whitelist as REW)


def generate_events_for_one_gamestate(options: RainWorldOptions,
                                      regions: list[RainWorldRegion]) -> list[StaticWorldEvent]:
    ret = []
    scugs = scugs_all if options.dlcstate == "MSC" else scugs_vanilla

    for region in regions:
        if (rooms := region.rooms) and len(rooms) > 0:
            if region_data := options.data_block.get(region.code[:2], {}):
                events: dict[str, GameStateFlag] = {}

                for room in rooms:
                    if room_data := region_data.get(room, {}):
                        for obj_type, obj_data in room_data.get("objects", {}).items():
                            flag = events.setdefault(obj_type, GameStateFlag(0))
                            flag[options.dlcstate, POEW(room_data, obj_data, set(scugs))] = True

                        for crit_type, crit_data in room_data.get("spawners", {}).get("normal", {}).items():
                            flag = events.setdefault(crit_type, GameStateFlag(0))
                            flag[options.dlcstate, CDEW(room_data, crit_data, set(scugs))] = True

                        if room_tags := room_data.get("tags", []):
                            for tagname, eventname in (
                                    ("SWARMROOM", "Fly"), ("SCAVOUTPOST", "Toll"), ("SHELTER", "Shelter")
                            ):
                                if tagname in room_tags:
                                    flag = events.setdefault(eventname, GameStateFlag(0))
                                    flag[options.dlcstate, REW(room_data, set(scugs))] = True

                for event_type, event_flag in events.items():
                    if options.satisfies(event_flag):
                        ret.append(StaticWorldEvent(event_type, f'{region.name} {event_type}', region.name))

    # HARDCODE
    for room in ("SS_E07", "SL_AI", "RM_AI", "DM_AI", "LC_LAB01"):
        ret.append(StaticWorldEvent("SSOracleSwarmer", f'{room} SSOracleSwarmer',
                                    room_to_region[room]))

    # HARDCODE: Yeeks spawn for Sofanthiel without dens.
    ret.append(StaticWorldEvent("Yeek", "Chimney Canopy gimmick", "Chimney Canopy", scugs={"Inv"}))

    if options.starting_scug in {"Yellow", "White", "Red", "Gourmand", "Rivulet", "Saint"}:
        ret.append(StaticWorldEvent("Meet LttM", f'{room} LttM', room_to_region["SL_AI"], Simple("The Mark")))

    return ret
