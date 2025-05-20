from random import Random

from BaseClasses import MultiWorld
from .classes import RegionData, ConnectionData, room_to_region
from ..options import RainWorldOptions
from ..conditions.classes import Simple, ConditionBlank, AllOf
from ..game_data.watcher import targets, normal_regions
from ..game_data.general import region_code_to_name
from ..utils import random_bijective_endofunction


class DynamicWarpConnection(ConnectionData):
    def __init__(self, source: str, dest: str, ripple: float | None, sort: str,
                 source_room: bool = True, target_room: bool = True):
        self.ripple, self.source_room, self.target_room = ripple, source_room, target_room
        cond = Simple("Ripple", int((ripple - 1) * 2)) if ripple is not None else ConditionBlank
        super().__init__(source, dest, f"{sort} dynamic warp to {dest} ({ripple})", cond)

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        self.source = room_to_region[self.source] if self.source_room else self.source
        self.dest = room_to_region[self.dest] if self.target_room else self.dest
        super().make(player, multiworld, options)


class NormalDynamic(DynamicWarpConnection):
    def __init__(self, dest: str, ripple: float):
        super().__init__("From any normal region", dest, ripple, "Normal", False, True)


class PredeterminedNormalDynamic(DynamicWarpConnection):
    def __init__(self, source: str, dest: str, ripple: float):
        self.region_code = source
        super().__init__(region_code_to_name[source], dest, ripple, "Predetermined normal", False, True)

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        multiworld.worlds[player].predetermined_warps[self.region_code] = self.dest
        super().make(player, multiworld, options)


class PredeterminedThroneDynamic(DynamicWarpConnection):
    def __init__(self, dest: str, ripple: float, which: int):
        super().__init__(self.rooms[which], dest, ripple, f"{self.names[which]} Throne", True, True)

    rooms = [f"WORA_THRONE{a:0>2}" for a in (10, 5, 9, 7)]
    names = ["Lower east", "Lower west", "Upper east", "Upper west"]

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        multiworld.worlds[player].predetermined_warps[self.source] = self.dest
        super().make(player, multiworld, options)


class StaticPoolNormalDynamic(DynamicWarpConnection):
    def __init__(self, dest: str, ripple: float | None):
        super().__init__("From any normal region", dest, ripple, "Normal", False, True)

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        multiworld.worlds[player].normal_pool.append(self.dest)
        super().make(player, multiworld, options)


class UnlockablePoolNormalDynamic(DynamicWarpConnection):
    def __init__(self, dest: str, ripple: float | None):
        super().__init__("From any normal region", dest, ripple, "Normal", False, True)
        self.condition = AllOf(self.condition, Simple(f"Dynamic: {dest[:4]}"))

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        multiworld.worlds[player].unlockable_pool.append(self.dest[:4])
        super().make(player, multiworld, options)


def generate(options: RainWorldOptions, rng: Random):
    if options.starting_scug != "Watcher":
        return []

    ret = [
        RegionData("From any normal region"),

        ConnectionData("Menu", "From any normal region", "Create a dynamic warp", Simple("Ripple", 2)),
        ConnectionData("From any normal region", "Crumbling Fringes", "Bad dynamic warp to Crumbling Fringes"),
        ConnectionData("From any normal region", "Corrupted Factories", "Bad dynamic warp to Corrupted Factories"),
        ConnectionData("From any normal region", "Decaying Tunnels", "Bad dynamic warp to Decaying Tunnels"),
        ConnectionData("From any normal region", "Infested Wastes", "Bad dynamic warp to Infested Wastes"),
    ]

    ####################################################################################################################
    match options.normal_dynamic_warp_behavior:
        case 3:  # open world
            for target in targets:
                ret.append(NormalDynamic(target.room, target.ripple))

        case "predetermined":
            for source, target_region in random_bijective_endofunction(normal_regions, rng).items():
                target = rng.sample([t for t in targets if t.room.startswith(target_region)], 1)[0]
                ret.append(PredeterminedNormalDynamic(source, target.room, target.ripple))

        case "static_pool":
            if (size := int(options.dynamic_warp_pool_size)) == 18:
                pool = normal_regions
            else:
                pool = rng.sample(normal_regions, size - 1)
                # Ensure that at least one of the options has a target with a Ripple requirement of 1.0.
                if len(set(pool).intersection(ripple_one_targets := ['WRFA', 'WSKB', 'WARF', 'WSKA'])) == 0:
                    pool[0] = rng.choice(ripple_one_targets)

            for target in [t for t in targets if any(t.room.startswith(r) for r in pool)]:
                ret.append(StaticPoolNormalDynamic(target.room, target.ripple))

        case "unlockable_pool":
            if (size := int(options.dynamic_warp_pool_size)) == 18:
                pool = normal_regions
            else:
                pool = rng.sample(normal_regions, size)

            for target in [t for t in targets if any(t.room.startswith(r) for r in pool)]:
                ret.append(UnlockablePoolNormalDynamic(target.room, target.ripple))

    ####################################################################################################################
    match options.throne_dynamic_warp_behavior:
        case "predetermined":
            chosen = rng.sample(normal_regions, 4)
            chosen = [rng.choice([t for t in targets if t.room.startswith(reg)]) for reg in chosen]
            chosen = sorted([c for c in chosen], key=lambda x: x.ripple)

            for i, target in enumerate(chosen):
                ret.append(PredeterminedThroneDynamic(target.room, i + 2, i))

    return ret



