from BaseClasses import MultiWorld
from .classes import RoomLocation
from ..conditions import GameStateFlag
from ..conditions.classes import Simple
from ..game_data.general import scugs_all, scugs_vanilla
from ..options import RainWorldOptions
from ..game_data import static_data
from ..regions.classes import room_to_region

name_format = {
    "BlueToken": "Arena Token - {0}",
    "GreenToken": "Arena Token - {0}",
    "GoldToken": "Level Token - {0}",
    "RedToken": "Safari Token",
    "WhiteToken": "Broadcast - {0}",
    "DevToken": "Dev Token - {0}",
    "UniqueDataPearl": "Pearl - {0}",
    "DataPearl": "Pearl - {0}",
}


class TokenOrPearl(RoomLocation):
    def __init__(self, name: str, kind: str, r: str, offset: int, old_name: str):
        super().__init__(name_format[kind].format(name), old_name, [], offset, r)
        self.generation_flag = GameStateFlag(0)
        self.room = r
        self.kind = kind

    def pre_generate(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        if self.kind == "DevToken":
            return False
        if self.kind == "WhiteToken":
            if not (options.msc_enabled and (options.starting_scug == "Spear") + options.checks_broadcasts.value >= 2):
                return False
        if not options.satisfies(self.generation_flag):
            return False

        # HARDCODE: This specific token doesn't appear for Hunter - not sure why.
        if options.starting_scug == "Red" and self.client_name == "Token-Scavenger-GW":
            return False
        # HARDCODE: This token is far underwater and GW doesn't have Bubble Weed.
        if self.client_name == "Token-RedLizard-GW":
            self.access_condition = Simple("BubbleGrass")

        self.region = room_to_region[self.room]
        return super().pre_generate(player, multiworld, options)


def token_name(name: str, kind: str, _region: str) -> str:
    if kind == "GoldToken":  # arena level unlock
        return f'Token-L-{name}'
    elif kind == "RedToken":  # safari level unlock
        return f'Token-S-{name}'
    elif kind == "WhiteToken":
        return f'Broadcast-{name}-{_region}'
    elif kind == "DevToken":
        return f'DevToken-{name}-{_region}'
    elif "Token" in kind:
        return f'Token-{name}-{_region}'
    else:
        return f'Pearl-{name}-{_region}'


def initialize() -> dict[str, TokenOrPearl]:
    offset = 0
    ret = {}

    for scuglist, (dlcstate, dlcstate_data) in zip((scugs_vanilla, scugs_all), static_data.items()):
        for region, region_data in dlcstate_data.items():
            for room, room_data in region_data.items():
                if "shinies" in room_data.keys():
                    for shiny_name, shiny_data in room_data["shinies"].items():
                        name = token_name(shiny_name, shiny_data["kind"], region)
                        if (loc := ret.get(name, None)) is None:
                            loc = TokenOrPearl(shiny_name, shiny_data["kind"], room, offset, name)
                            ret[name] = loc
                            offset += 1

                        can_see = (
                            room_data.get("whitelist", set(scuglist))
                            .difference(room_data.get("blacklist", set()))
                            .difference(shiny_data.get("filter", set()))
                            .difference(room_data.get("alted", set()))
                            .union(shiny_data.get("whitelist", set()))
                            .difference({""})
                        )
                        loc.generation_flag[dlcstate, can_see] = True

    return ret


locations = initialize()


def generate(_: RainWorldOptions) -> list[RoomLocation]:
    return list(locations.values())
