from ..game_data.files import rooms as all_rooms
from ..game_data.general import scugs_all, scugs_vanilla
from ..options import RainWorldOptions
from .classes import RoomData, ConnectionData


def generate(options: RainWorldOptions) -> tuple[list[RoomData], list[ConnectionData]]:
    rooms, conns = [], {}

    data = all_rooms["MSC" if options.msc_enabled else "Vanilla"]
    scugs = set(scugs_all if options.msc_enabled else scugs_vanilla)
    for region, region_data in data.items():
        for room, room_data in region_data.items():
            s = scugs
            if "whitelist" in room_data.keys():
                s = room_data["whitelist"]
            if "blacklist" in room_data.keys():
                s = s.difference(set(room_data["blacklist"]))

            rooms.append(RoomData(room, s))

            for conn in room_data["connections"]:
                conns[conn] = ConnectionData(room, conn, s)

            if "conditional" in room_data.keys():
                for scug, scug_data in room_data["conditional"].items():
                    if "new" in scug_data.keys():
                        for conn in scug_data["new"]:
                            if conn in conns.keys():
                                conns[conn].scugs.add(scug)
                            else:
                                conns[conn] = ConnectionData(room, conn, {scug})

                    if "replace" in scug_data.keys():
                        for old_conn, new_conn in scug_data["replace"].items():
                            conns[old_conn].scugs.remove(scug)
                            if new_conn in conns.keys():
                                conns[new_conn].scugs.add(scug)
                            else:
                                conns[new_conn] = ConnectionData(room, new_conn, {scug})

    return rooms, list(conns.values())

