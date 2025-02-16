# from .classes import LocationData
# from ..game_data.files import white_tokens
# from ..game_data.general import region_code_to_name
# from ..options import RainWorldOptions
#
# offset: int
# locations = [
#     LocationData(
#         f"Broadcast-{name}", f"Broadcast-{name}", region_code_to_name[data["room"].split("_")[0]], 5350 + offset
#     )
#     for offset, (name, data) in enumerate(white_tokens.items())
# ]
#
#
# def generate(options: RainWorldOptions) -> list[LocationData]:
#     if options.checks_broadcasts.value == 0:
#         return []
#     if options.starting_scug == "Spear" or options.checks_broadcasts.value == 2:
#         return locations
#     return []
