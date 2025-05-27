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
#     dlcstate ("Vanilla" | "MSC")
#       region code
#         room name
#           "whitelist": set of whitelisted scugs
#           "blacklist": set of blacklisted scugs
#           "broken"?: set of scugs for which this shelter is broken
#           "alted": set of scugs with alternate settings files
#           "tags": set of room tags
#           "spawners"
#             den type ("normal" | "precycle" | "lineage_start" | "lineage_mid" | "lineage_end")
#               creature type: set of whitelisted scugs
#           "shinies"
#             shiny name
#               "filter": set of filtered scugs
#               "whitelist": set of whitelisted scugs
#               "kind": token/pearl type
#           "objects"
#             object type
#               "filter": set of filtered scugs
#               "whitelist": set of whitelisted scugs
