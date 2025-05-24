from random import Random

from . import physical, classes, abstract, gates, portals, warping
from ..options import RainWorldOptions


def generate(options: RainWorldOptions, rng: Random) -> list[classes.RegionData | classes.ConnectionData]:
    return [
        *abstract.generate(options),
        *physical.generate(options),
        *gates.generate(options),
        *portals.generate(options),
        *warping.generate(options, rng),
    ]
