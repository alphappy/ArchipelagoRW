from . import passages, echoes, foodquest, unique, tokens_pearls, shelters, portals
from .classes import LocationData
from ..options import RainWorldOptions

# ID OFFSET BLOCKS:
# Tokens/Pearls        0 -  999
# Unique            4900 - 4999
# Passages          5000 - 5046
# Echoes            5070 - 5080
# Food Quest        5250 -~5301
# Shelters          5350 -~5550
# Fixed warps       6000 -~6100


def generate(options: RainWorldOptions) -> list[LocationData]:
    return [
        *tokens_pearls.generate(options),
        *unique.generate(options),
        *passages.generate(options),
        *echoes.generate(options),
        *shelters.select(options),
        *portals.select(options),
    ]


def generate_foodquest(options: RainWorldOptions) -> list[LocationData]:
    return foodquest.generate(options)
