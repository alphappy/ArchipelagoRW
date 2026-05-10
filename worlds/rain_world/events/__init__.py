from . import world, misc, victory
from .. import RainWorldOptions
from ..regions.classes import RainWorldRegion


def get_events(options: RainWorldOptions, regions: list[RainWorldRegion]):
    # This is sorted to prevent determinism issues
    return sorted([
        *world.generate_events_for_one_gamestate(options, regions),
        *victory.generate(options),
        *misc.generate_events(),
    ], key=lambda e: e.item_name)
