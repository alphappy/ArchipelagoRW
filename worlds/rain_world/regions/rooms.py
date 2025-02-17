from ..game_data import static_data
from ..game_data.general import scugs_all, scugs_vanilla
from ..options import RainWorldOptions
from .classes import RoomData, ConnectionData, RoomConnection


def _gate_check(name: str, region: str) -> str:
    return f'{name.upper()}[{region}]' if name.startswith("GATE_") or name.startswith("OFFSCREEN") else name.upper()


def _regional_whitelist(region: str, scugs: set[str]) -> set[str]:
    d = {
        "LM": {"Spear", "Artificer"},
        "DM": {"Spear"},
        "SL": scugs.difference({"Spear", "Artificer"}),
        "DS": scugs.difference({"Saint"}),
        "UG": {"Saint"},
        "CL": {"Saint"},
        "HR": {"Saint"},
        "SS": scugs.difference({"Saint", "Rivulet"}),
        "RM": {"Rivulet"},
        "MS": scugs.difference({"Spear", "Artificer"}),
        "OE": {"Yellow", "White", "Gourmand"},
        "LC": {"Artificer"},
        "SH": scugs.difference({"Saint"}),
        "UW": scugs.difference({"Saint"}),
    }
    d.setdefault(region, scugs)

    return d[region]


def generate(options: RainWorldOptions) -> tuple[list[RoomData], list[RoomConnection]]:
    rooms, conns = [], []

    data = static_data["MSC" if options.msc_enabled else "Vanilla"]
    for region, region_data in data.items():
        regional_whitelist = _regional_whitelist(region, set(scugs_all if options.msc_enabled else scugs_vanilla))

        for room, room_data in region_data.items():
            s = regional_whitelist
            if "whitelist" in room_data.keys():
                s = room_data["whitelist"]
            if "blacklist" in room_data.keys():
                s = s.difference(room_data["blacklist"])

            room = _gate_check(room, region)
            room_conns = {}

            rooms.append(RoomData(room, s))

            if "connections" in room_data.keys():
                for conn in room_data["connections"]:
                    conn = _gate_check(conn, region)
                    if conn != "DISCONNECTED":
                        room_conns[conn] = RoomConnection(room, conn, s)

            if "conditional" in room_data.keys():
                for scug, scug_data in room_data["conditional"].items():
                    if "new" in scug_data.keys():
                        for conn in scug_data["new"]:
                            conn = _gate_check(conn, region)
                            try:
                                room_conns[conn].scugs.add(scug)
                            except KeyError:
                                room_conns[conn] = RoomConnection(room, conn, {scug})

                    if "replace" in scug_data.keys():
                        for old_conn, new_conn in scug_data["replace"].items():
                            old_conn = _gate_check(old_conn, region)
                            new_conn = _gate_check(new_conn, region)
                            try:
                                room_conns[old_conn].scugs.remove(scug)
                            except KeyError:
                                pass

                            if new_conn != "DISCONNECTED":
                                try:
                                    room_conns[new_conn].scugs.add(scug)
                                except KeyError:
                                    room_conns[new_conn] = RoomConnection(room, new_conn, {scug})

            conns += list(room_conns.values())

    return rooms, conns

