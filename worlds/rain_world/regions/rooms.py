from ..game_data.files import rooms as all_rooms
from ..game_data.general import scugs_all, scugs_vanilla
from ..options import RainWorldOptions
from .classes import RoomData, ConnectionData, RoomConnection


def _gate_check(name: str, region: str) -> str:
    return f'{name.upper()}[{region}]' if name.startswith("GATE_") else name.upper()


def generate(options: RainWorldOptions) -> tuple[list[RoomData], list[RoomConnection]]:
    rooms, conns = [], []

    data = all_rooms["MSC" if options.msc_enabled else "Vanilla"]
    scugs = set(scugs_all if options.msc_enabled else scugs_vanilla)
    for region, region_data in data.items():
        for room, room_data in region_data.items():
            s = scugs
            if "whitelist" in room_data.keys():
                s = room_data["whitelist"]
            if "blacklist" in room_data.keys():
                s = s.difference(set(room_data["blacklist"]))

            room = _gate_check(room, region)
            room_conns = {}

            rooms.append(RoomData(room, s))

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

