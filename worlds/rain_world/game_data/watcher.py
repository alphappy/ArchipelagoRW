from ..game_data import static_data
from ..game_data.general import region_code_to_name


class PortalData:
    def __init__(self, source_room: str, data: dict, kind: str):
        self.source_room = source_room
        self.oneway, self.spinning_top, self.check_spinning_top = False, False, False

        if kind == "WarpPoint":
            oneway, entrance, self.ripple = [(data['flags'] >> i) & 1 != 0 for i in range(3)]
            self.oneway = oneway and entrance
            self.target_room = data['to'].upper()

        elif kind == "SpinningTop":
            self.ripple = data['ripple']
            self.oneway = True  # TODO
            self.target_room = data['to'].upper()
            self.spinning_top = True
            self.check_spinning_top = not self.source_room.startswith("WAUA")

        # See `OverWorld.InitiateSpecialWarp_WarpPoint`.
        if self.target_room == "NULL":
            if self.source_room[3] == "R":  # rotted FP region
                self.target_room = "WORA_START"  # TODO this needs to be a room in lower WORA
            elif self.source_room.startswith("WARA"):
                self.target_room = "WAUA_E01"  # first WAUA spawn
            elif self.source_room.startswith("WAUA"):
                # WAUA STs logically don't go anywhere.
                # At time of writing, not sure what's up with the SB_D07 target. TODO
                self.target_room = self.source_room
            elif self.ripple:
                self.target_room = "WRSA_L01"  # Daemon
            elif self.source_room == "WORA_DESERT6":
                self.target_room = "WORA_DESERT6"
            else:  # some non-ripple warp isn't covered
                raise Exception("There's a portal that doesn't make sense: "
                                f"{self.source_room}->{self.target_room} "
                                f"({self.ripple} {self.oneway} {self.spinning_top})")

    @property
    def key_name(self):
        a, b = sorted(region_code_to_name[x.split("_")[0].upper()] for x in (self.source_room, self.target_room))
        return f"Warp: {a} / {b}"

    @property
    def should_have_key(self) -> bool:
        source_region = self.source_room.upper().split("_")[0]
        target_region = self.target_room.upper().split("_")[0]
        if source_region == "WORA":
            return target_region == "WRSA"
        elif any(x == source_region or x == target_region for x in ["WORA", "WAUA", "WSUR", "WHIR", "WGWR", "WDSR"]):
            return False
        elif source_region == "WRSA":  # to RSA may have keys, but from RSA may not
            return False
        return True


class PortalKeyData:
    def __init__(self, source: str, dest: str, spinning_top: bool, name: str):
        self.source, self.dest, self.spinning_top, self.name = source, dest, spinning_top, name


class WarpTargetData:
    def __init__(self, room: str, ripple: float):
        self.room, self.ripple = room, ripple


def initialize() -> tuple[list[PortalData], dict[str, PortalKeyData], list[WarpTargetData]]:
    ret = [
        *[PortalData(k, v, "WarpPoint") for k, v in static_data['SPECIAL']['Watcher']['WarpPoints'].items()],
        *[PortalData(k, v, "SpinningTop") for k, v in static_data['SPECIAL']['Watcher']['SpinningTops'].items()],
    ]

    ret2 = {}
    for data in [r for r in ret if r.should_have_key]:
        s, t = data.source_room.split("_")[0].upper(), data.target_room.split("_")[0].upper()
        n = "".join(sorted([s, t]))

        ret2.setdefault(n, PortalKeyData(s, t, data.spinning_top, data.key_name))

    ret3 = []
    for room, warpdata in static_data['SPECIAL']['Watcher']['DynamicWarpTargets'].items():
        if warpdata['flags'] >> 1 == 0:  # not a bad warp target
            ret3.append(WarpTargetData(room, warpdata['req']))

    return ret, ret2, ret3


portals, keys, targets = initialize()

normal_regions = [
    'WVWA', 'WRFB', 'WRFA', 'WSKA', 'WPTA', 'WRRA', 'WSKB', 'WARF', 'WTDB',
    'WARE', 'WTDA', 'WSKC', 'WARD', 'WARB', 'WARC', 'WBLA', 'WARG', 'WSKD',
]
