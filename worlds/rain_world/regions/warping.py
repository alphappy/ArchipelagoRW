from itertools import cycle, pairwise
from random import Random

from BaseClasses import MultiWorld
from .classes import RegionData, ConnectionData, room_to_region
from ..options import RainWorldOptions
from ..conditions.classes import Simple, ConditionBlank, AllOf
from ..game_data.watcher import targets, normal_regions, abnormal_regions
from ..game_data.general import region_code_to_name
from ..utils import necklace_derangement


class DynamicWarpConnection(ConnectionData):
    def __init__(self, source: str, dest: str, ripple: float | None, sort: str,
                 source_room: bool = True, target_room: bool = True):
        self.ripple, self.source_room, self.target_room = ripple, source_room, target_room
        cond = Simple("Ripple", int((ripple - 1) * 2)) if ripple is not None else ConditionBlank
        super().__init__(source, dest, f"{sort} dynamic warp from {source} to {dest} ({ripple})", cond)

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        self.source = room_to_region[self.source] if self.source_room else self.source
        self.dest = room_to_region[self.dest] if self.target_room else self.dest
        super().make(player, multiworld, options)


class NormalDynamic(DynamicWarpConnection):
    def __init__(self, dest: str, ripple: float):
        super().__init__("From any normal region", dest, ripple, "Normal", False, True)


class PredeterminedNormalDynamic(DynamicWarpConnection):
    def __init__(self, source: str, dest: str, ripple: float, unlockable: bool = False):
        self.region_code = source
        self.unlockable = unlockable
        super().__init__(region_code_to_name[source], dest, ripple, "Predetermined normal", False, True)
        if unlockable:
            self.condition = AllOf(self.condition, Simple(f"Dynamic: {self.region_code}"))

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


class PoolNormalDynamic(DynamicWarpConnection):
    def __init__(self, dest: str, ripple: float | None, unlockable: bool = False):
        self.unlockable = unlockable
        self.dest_region = dest.split("_")[0]
        super().__init__("From any normal region", dest, ripple, "Normal", False, True)
        if unlockable:
            self.condition = AllOf(self.condition, Simple(f"Dynamic: {self.dest_region}"))

    def make(self, player: int, multiworld: MultiWorld, options: RainWorldOptions):
        multiworld.worlds[player].warp_pool.add(self.dest_region if self.unlockable else self.dest)
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
    pool_size = int(options.dynamic_warp_pool_size)
    pool = normal_regions if pool_size == 18 else rng.sample(normal_regions, pool_size)
    mnl = options.predetermined_dynamic_warp_network_minimum_necklace_length.value

    if (bhv := options.normal_dynamic_warp_behavior).predetermined:
        # Map targets not in the pool to targets in the pool for replacement.
        # Cycle the pool to get an even distribution of replacements for small pools.
        # Pairwise the pool so there is a second option if it would replace a region's target with itself.
        pool_sampler = pairwise(cycle(pool))
        replacing = dict(zip(list(set(normal_regions).difference(set(pool))), pool_sampler))

        # Generate a derangement of the normal regions.  Add the abnormal regions to the mapping.
        mapping = necklace_derangement(normal_regions, rng, mnl)
        mapping.update({k: v[0] for k, v in zip(abnormal_regions, pool_sampler)})

        for source, target_region in mapping.items():
            # Get the potential replacements for this target if it is not in the pool.
            rep1, rep2 = replacing.get(target_region, (target_region, target_region))
            # Replace the target region, but not with the source region.
            target_region = rep1 if rep1 != source else rep2
            # Pick a random DynamicWarpTarget in the region and create the connection.
            target = rng.sample([t for t in targets if t.room.startswith(target_region)], 1)[0]
            ret.append(PredeterminedNormalDynamic(source, target.room, target.ripple, bhv.unlockable))

    else:
        # For static pool, ensure that at least one target region is ripple level 1.
        if not (bhv.unlockable or set(pool).intersection(ripple_one_targets := ['WRFA', 'WSKB', 'WARF', 'WSKA'])):
            pool[0] = rng.choice(ripple_one_targets)

        for target in [t for t in targets if any(t.room.startswith(r) for r in pool)]:
            ret.append(PoolNormalDynamic(target.room, target.ripple, bhv.unlockable))

    ####################################################################################################################
    if options.throne_dynamic_warp_behavior == "static_predetermined":
        # Choose 4 regions.  Pick a target in each.  Sort them by their Ripple level requirement.
        chosen = rng.sample(normal_regions, 4)
        chosen = [rng.choice([t for t in targets if t.room.startswith(reg)]) for reg in chosen]
        chosen = sorted([c for c in chosen], key=lambda x: x.ripple)

        for i, target in enumerate(chosen):
            ret.append(PredeterminedThroneDynamic(target.room, i + 2, i))

    return ret



