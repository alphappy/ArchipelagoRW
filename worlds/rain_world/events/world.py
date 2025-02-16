from .classes import ObjectEventData2
from ..options import RainWorldOptions

from ..game_data.general import scugs_all, scugs_vanilla
from ..conditions.classes import Simple, AnyOf, AllOf
from ..game_data import static_data


# def generate_events_for_one_gamestate(which: str, options: RainWorldOptions) -> list[ObjectEventData2]:
#     dlcstate = "MSC" if options.msc_enabled else "Vanilla"
#     scug = options.starting_scug
#
#     ret = []
#     data = placed_objects if which == "placed_objects" else creatures["normal"]
#
#     for otype, by_otype in data.items():
#         regions = set(room.split("_")[0] for room in by_otype[dlcstate][scug] + by_otype[dlcstate]["*ALL"])
#
#         if len(regions) != 0:
#             condition = \
#                 AllOf(
#                     Simple("MSC", negative=not options.msc_enabled),
#                     Simple(f"Scug-{scug}"),
#                     Simple([f"Access-{region}" for region in regions], 1)
#                 )
#             ret.append(ObjectEventData2(otype, otype, "Events", condition, regions))
#
#     return ret
