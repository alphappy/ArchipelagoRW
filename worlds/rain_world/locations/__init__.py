from . import passages, echoes, foodquest, unique, tokens_pearls, shelters, watcher, flowers
from .classes import LocationData
from ..options import RainWorldOptions

# ID OFFSET BLOCKS:
# Tokens/Pearls        0 -  999
# Flowers           1200 -~1700
# Unique            4900 - 4999
# Passages          5000 - 5046
# Echoes            5070 - 5080
# Food Quest        5250 -~5301
# Shelters          5350 -~5750
# Fixed warps       6000 -~6100
# Spinning Tops     6100 -~6115
# Prince encounters 6120 - 6123
# Throne warp       6125 - 6128
# Rot spread        6130 - 6147


def generate(options: RainWorldOptions) -> list[LocationData]:
    return [
        *tokens_pearls.generate(options),
        *flowers.select(options),
        *unique.generate(options),
        *passages.generate(options),
        *echoes.generate(options),
        *shelters.select(options),
        *watcher.select(options),
    ]


def generate_foodquest(options: RainWorldOptions) -> list[LocationData]:
    return foodquest.generate(options)
