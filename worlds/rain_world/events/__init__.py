from . import world, misc, victory
from .. import RainWorldOptions


def get_events(options: RainWorldOptions):
    return [
        # *world.generate_events_for_one_gamestate("placed_objects", options),
        # *world.generate_events_for_one_gamestate("creatures", options),
        *victory.generate(options),
        # *misc.generate_events(),
    ]
