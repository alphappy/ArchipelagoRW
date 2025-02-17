from typing import Callable

from BaseClasses import MultiWorld
from .classes import LocationData
from ..options import RainWorldOptions
from ..game_data.files import tokens_pearls
from ..game_data.general import region_code_to_name, scugs_all, scugs_vanilla
from ..conditions.classes import AnyOf, AllOf, Simple, Condition

locations = {}
next_offset = 0


class TokenOrPearl(LocationData):
    def __init__(self, name: str, region: str, offset: int,
                 msc_blacklist: list[str] | None = None,
                 vanilla_blacklist: list[str] | None = None):
        super().__init__(name, name, region, offset)
        self.msc_blacklist = msc_blacklist
        self.vanilla_blacklist = vanilla_blacklist

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions) -> bool:
        # HARDCODE: This pearl only appears in a past-GW room.
        if self.full_name == "Pearl-MS-GW":
            self.msc_blacklist = set(scugs_all).difference({"Artificer", "Spear"})
        # HARDCODE: This pearl isn't accessible from SU proper.
        if self.full_name == "Pearl-SU_filt-SU":
            self.region = "Outskirts filtration"

        self.generation_condition = self._gen()
        # self.access_condition = self._acc()
        return super().make(player, multiworld, options)

    def _gen(self) -> Callable[[RainWorldOptions], bool]:
        def inner(options: RainWorldOptions) -> bool:
            if self.full_name.startswith("DevToken"):
                return False
            # HARDCODE: This pearl only appears in a past-GW room.
            if options.checks_tokens_pearls and self.full_name != "Pearl-MS-GW":
                return True
            if options.msc_enabled and options.starting_scug not in (self.msc_blacklist or []):
                return True
            if not options.msc_enabled and options.starting_scug not in (self.vanilla_blacklist or []):
                return True
            return False
        return inner

    def _acc(self, options: RainWorldOptions) -> Condition:
        return \
            AnyOf(
                AllOf(
                    Simple("MSC"),
                    Simple([f'Scug-{scug}' for scug in set(scugs_all).difference(set(self.msc_blacklist))], 1)
                ),
                AllOf(
                    Simple("MSC", negative=True),
                    Simple([f'Scug-{scug}' for scug in set(scugs_vanilla).difference(set(self.vanilla_blacklist))], 1)
                )
            )


def token_name(obj: dict) -> str:
    _region = obj["room"].split("_")[0]

    if obj["type"] == "GoldToken":  # arena level unlock
        return f'Token-L-{obj["name"]}'
    elif obj["type"] == "RedToken":  # safari level unlock
        return f'Token-S-{obj["name"]}'
    elif obj["type"] == "DevToken":
        return f'DevToken-{obj["name"]}-{_region}'
    elif "Token" in obj["type"]:
        return f'Token-{obj["name"]}-{_region}'
    else:
        return f'Pearl-{obj["name"]}-{_region}'


for obj in tokens_pearls["MSC"]:
    if "Pearl" in obj["type"] and (obj["name"].startswith("Misc") or obj["name"].strip() == ''):
        continue
    if "WhiteToken" in obj["type"]:
        continue

    name = token_name(obj)
    region = obj["room"].split("_")[0]
    locations[name] = TokenOrPearl(token_name(obj), region_code_to_name[region], next_offset,
                                   msc_blacklist=obj["blacklist"])
    next_offset += 1


for obj in tokens_pearls["Vanilla"]:
    if "Pearl" in obj["type"] and (obj["name"].startswith("Misc") or obj["name"].strip() == ''):
        continue

    name = token_name(obj)

    if name in locations.keys():
        locations[name].vanilla_blacklist = obj["blacklist"]
    else:
        region = obj["room"].split("_")[0]
        locations[name] = TokenOrPearl(token_name(obj), region_code_to_name[region], next_offset,
                                       vanilla_blacklist=obj["blacklist"])
        next_offset += 1


def generate(_: RainWorldOptions) -> list[LocationData]:
    return list(locations.values())
