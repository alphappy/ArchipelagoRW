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


def placed_object_effective_whitelist(room_data: dict, shiny_data: dict, scuglist: set[str]) -> set[str]:
    return (
        room_data.get("whitelist", set(scuglist))
        .difference(room_data.get("blacklist", set()))
        .difference(shiny_data.get("filter", set()))
        .difference(room_data.get("alted", set()))
        .union(shiny_data.get("whitelist", set()))
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


