from typing import Callable

from BaseClasses import MultiWorld
from .classes import LocationData
from ..conditions import GameStateFlag
from ..options import RainWorldOptions
from ..game_data import static_data
from ..utils import effective_blacklist
from ..regions.classes import room_to_region

locations = {}
next_offset = 0


class TokenOrPearl(LocationData):
    def __init__(self, name: str, r: str, offset: int, flag: GameStateFlag | None = None):
        super().__init__(name, name, r, offset)
        self.generation_flag = flag or GameStateFlag(0)
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


for region, region_data in static_data["MSC"].items():
    for room, room_data in region_data.items():
        if "shinies" in room_data.keys():
            for shiny_name, shiny_data in room_data["shinies"].items():
                name = token_name(shiny_name, shiny_data["kind"], region)
                locations[name] = TokenOrPearl(
                    name, room, next_offset,
                    GameStateFlag(
                        msc=effective_blacklist(
                            shiny_data.get("filter", None), shiny_data.get("whitelist", None), room_data
                        )
                    )
                )
                next_offset += 1


for region, region_data in static_data["Vanilla"].items():
    for room, room_data in region_data.items():
        if "shinies" in room_data.keys():
            for shiny_name, shiny_data in room_data["shinies"].items():
                name = token_name(shiny_name, shiny_data["kind"], region)
                if name in locations.keys():
                    locations[name].generation_flag["Vanilla", shiny_data.get("filter", set()).difference({""})] = False
                else:
                    locations[name] = TokenOrPearl(
                        name, room, next_offset,
                        GameStateFlag(
                            vanilla=effective_blacklist(
                                shiny_data.get("filter", None), shiny_data.get("whitelist", None), room_data
                            )
                        )
                    )
                    next_offset += 1


def generate(_: RainWorldOptions) -> list[LocationData]:
    return list(locations.values())
