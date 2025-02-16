"""
Static data summarizing the contents of the game world, such as the locations of creature spawns.
"""

from . import general
from .data import data as static_data

# static_data structure:
# (root)
#   dlcstate ("Vanilla" | "MSC")
#     region code
#       room name
#         "connections": list of destination rooms
#         "tags": list of room tags
#         "whitelist": set of whitelisted scugs
#         "blacklist": set of blacklisted scugs
#         "conditional"
#           scugname
#             "new": list of new connections
#             "replace"
#               connected room name: name of room to replace this connection
#         "spawners"
#           den type ("normal" | "precycle" | "lineage_start" | "lineage_mid" | "lineage_end")
#             creature type: set of whitelisted scugs
#         "shinies": list of objects
#           index
#             "name": token name
#             "blacklist": list of blacklisted scugs
#             "kind": token type
#         "objects"
#           object type: set of blacklisted scugs
