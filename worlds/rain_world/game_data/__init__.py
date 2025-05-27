"""
Static data summarizing the contents of the game world, such as the locations of creature spawns.
"""
__all__ = ['portals', 'static_data', 'general']

from . import general
from .data import data as static_data
from .generate_methods_post import recursive_flag_expansion
from .hardcode import apply_hardcoded_exceptions
from .watcher import portals

recursive_flag_expansion(static_data)
apply_hardcoded_exceptions(static_data)

# (root)
#   game version ("1.9.15.3" | "1.10.4")
#     dlcstate ("Vanilla" | "MSC" | "Watcher" | "MSC_Watcher")
#       region code, all caps
#         room name, all caps, including region code
#           "whitelist": ScugFlag for `EXCLUSIVEROOM`
#           "blacklist": ScugFlag for `HIDEROOM`
#           "broken"?: ScugFlag for broken shelters
#           "alted": ScugFlag for alternate room settings files
#           "tags": set of room tags
#           "spawners"
#             den type ("normal" | "precycle" | "lineage_start" | "lineage_mid" | "lineage_end")
#               creature type: ScugFlag of scugs that see this creature and den type
#           "shinies"
#             shiny name
#               "filter": ScugFlag of filtered scugs
#               "whitelist": ScugFlag of whitelisted scugs
#               "kind": token/pearl type
#           "objects"
#             object type
#               "filter": ScugFlag of filtered scugs
#               "whitelist": ScugFlag of whitelisted scugs
