from typing import Callable

from BaseClasses import MultiWorld
from .classes import LocationData
from ..conditions import GameStateFlag
from ..game_data.general import scugs_all, scugs_vanilla
from ..options import RainWorldOptions
from ..game_data import static_data
from ..regions.classes import room_to_region

locations = {}
next_offset = 0


class TokenOrPearl(LocationData):
    def __init__(self, name: str, r: str, offset: int, flag: GameStateFlag):
        super().__init__(name, name, r, offset)
        self.generation_flag = flag
        self.room = r

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        self.region = room_to_region[self.room]
        self.generation_condition = self._gen()
        return super().make(player, multiworld, options)

    def _gen(self) -> Callable[[RainWorldOptions], bool]:
        def inner(options: RainWorldOptions) -> bool:
            if self.full_name.startswith("DevToken"):
                return False
            if self.full_name.startswith("Broadcast"):
                return options.msc_enabled and (
                        (options.starting_scug == "Spear") + options.checks_broadcasts.value >= 2
                )
            if options.satisfies(self.generation_flag):
                return True
            return False
        return inner


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


for scuglist, (dlcstate, dlcstate_data) in zip((scugs_vanilla, scugs_all), static_data.items()):
    for region, region_data in dlcstate_data.items():
        for room, room_data in region_data.items():
            if "shinies" in room_data.keys():
                for shiny_name, shiny_data in room_data["shinies"].items():
                    name = token_name(shiny_name, shiny_data["kind"], region)
                    loc = locations.setdefault(name, TokenOrPearl(name, room, next_offset, GameStateFlag(0)))

                    can_see = (
                        room_data.get("whitelist", set(scuglist))
                        .difference(room_data.get("blacklist", set()))
                        .difference(shiny_data.get("filter", set()))
                        .difference(room_data.get("alted", set()))
                        .union(shiny_data.get("whitelist", set()))
                        .difference({""})
                    )
                    loc.generation_flag[dlcstate, can_see] = True

                    next_offset += 1


def generate(_: RainWorldOptions) -> list[LocationData]:
    return list(locations.values())
