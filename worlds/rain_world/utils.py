from random import Random
from typing import TypeVar

T = TypeVar("T")


def flatten(lol: list[list[T]]) -> list[T]:
    """Flattens a list of lists."""
    return [item for sublist in lol for item in sublist]


def normalize(d: dict[T, float]) -> dict[T, float]:
    """Normalizes a dictionary of weights so that all its weights add to 1."""
    total = sum(list(d.values()))
    return {k: v / total for k, v in d.items()}


def flounder2(weights: dict[T, float], count: int) -> list[T]:
    """Construct a list from a dictionary of weighted keys.
    Each key will appear a number of times in the list roughly proportional to its weight.
    In the event of a tie between remaining weights, preference goes to the earlier key.

    :param weights:  The dictionary of weights.  The nature of the keys is irrelevant.
    Each value represents the proportion that its corresponding key should make up of the resultant list.
    The weights do not need to already be normalized.
    :param count:  The length that the resultant list should have.
    :return:  The resultant list of length `count`, containing only keys of `weights`.
    """
    # Compute roughly how many entries each item should have.  The total number of credits is the `count`.
    credit = {k: v * count for k, v in normalize(weights).items()}
    # Compute the remainders for each credit value.
    remainders = {k: v - int(v) for k, v in credit.items()}

    ret = []
    # Each item is added to the list once for each full (integer) credit.
    for item, proportion in credit.items():
        ret += [item] * int(proportion)
    # Then, sort the credit values by their remainders and assign extras starting with the largest remainders
    # until the list reaches the appropriate size.
    for item, remainder in sorted(remainders.items(), key=lambda i: -i[1]):
        if len(ret) >= count:
            break
        ret.append(item)

    # Ensure that the return is exactly of length `count`.
    return ret[:count]


def random_bijective_endofunction(population: list[T], rng: Random, no_fixed_points: bool = True) -> dict[T, T]:
    """Generates a mapping in which every member of `population`
    appears exactly once as an input and exactly once as an output.
    If `no_fixed_points`, then members cannot be mapped to themselves."""
    shuffled = rng.sample(population, len(population))
    ret = {a: b for a, b in zip(population, shuffled)}
    if no_fixed_points:
        for number, fixed_point in enumerate(a for a, b in ret.items() if a == b):
            swap_key = list(ret.keys())[number]
            ret[swap_key], ret[fixed_point] = fixed_point, ret[swap_key]
    return ret


def necklace_derangement(pop: list[T], rng: Random) -> dict[T, T]:
    """Generates a derangement of `pop`."""
    # Generate a random partition of `len(pop)` with no numbers smaller than 3.  These are the necklace lengths.
    sizes = []
    remaining = len(pop)
    while remaining > 2:
        sizes.append(val := (3 if remaining == 3 else rng.randrange(3, remaining)))
        remaining -= val
    # If anything < 3 is left over, slap it onto a random necklace.
    sizes[rng.randrange(len(sizes))] += remaining

    # Shuffle the list.
    shuffled = rng.sample(pop, len(pop))
    targets = []
    cursor = 0
    # For each picked necklace size `n`...
    for size in sizes:
        # Take the next `n` targets up for consideration and shift them up one, wrapping the first one around.
        targets += shuffled[cursor + 1:cursor + size] + [shuffled[cursor]]
        cursor += size

    return dict(zip(pop, shuffled))


def placed_object_effective_whitelist(room_data: dict, shiny_data: dict, scuglist: set[str]) -> set[str]:
    maybe_whitelist = shiny_data.get("whitelist", set())

    return (
        room_data.get("whitelist", set(scuglist))
        .difference(room_data.get("blacklist", set()))
        .difference(shiny_data.get("filter", scuglist.difference(maybe_whitelist)))
        .difference(room_data.get("alted", set()))
        .union(maybe_whitelist)
        .difference({""})
    )


def creature_den_effective_whitelist(room_data: dict, den_data: set[str], scuglist: set[str]) -> set[str]:
    return (
        room_data.get("whitelist", set(scuglist))
        .difference(room_data.get("blacklist", set()))
        .intersection(den_data)
    )


def room_effective_whitelist(room_data: dict, scuglist: set[str]) -> set[str]:
    return (
        room_data.get("whitelist", set(scuglist))
        .difference(room_data.get("blacklist", set()))
        # .difference(room_data.get("alted", set()))  TODO this does matter but it can't be handled like this
        .difference({""})
    )


