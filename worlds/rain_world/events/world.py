from .classes import StaticWorldEvent
from ..options import RainWorldOptions
from ..game_data import static_data


def generate_events_for_one_gamestate(options: RainWorldOptions) -> list[StaticWorldEvent]:
    dlcstate = "MSC" if options.msc_enabled else "Vanilla"
    ret = []

    for region, region_data in static_data[dlcstate].items():
        for room, room_data in region_data.items():
            if "objects" in room_data.keys():
                for objtype, blacklist in room_data["objects"].items():
                    ret.append(StaticWorldEvent(objtype, f'{room} {objtype}', room))

    return ret
