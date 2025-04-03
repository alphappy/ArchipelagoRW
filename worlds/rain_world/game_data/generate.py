import re
from os import path
from glob import glob

from generate_classes import Spawner
from generate_methods import parse_placed_objects, splitstrip, setdefaultchain as sdc

########################################################################################################################
# Before the generator may run, a directory must be created to house each dlcstate's files.
# There should be a <ROOT_FP>/VERSION/DLCSTATE/world folder for each DLCSTATE (right now, just "Vanilla" and "MSC").
# To construct this (OUTDATED):
#   Run Rain World with MSC enabled and no other content mods that affect `world` files.
#   Locate your StreamingAssets folder (e.g., Steam\steamapps\common\Rain World\RainWorld_Data\StreamingAssets).
#   Copy StreamingAssets/world to <ROOT_FP>/Vanilla.
#   Delete <ROOT_FP>/Vanilla/world/gw-rooms/world-gw.txt.
#   Delete <ROOT_FP>/Vanilla/world/su/world-su - copy.txt.
#   Copy <ROOT_FP>/Vanilla to <ROOT_FP>/MSC.
#   Copy StreamingAssets/mergedmods/world to <ROOT_FP>/MSC, replacing any collisions.
#   Copy StreamingAssets/mods/moreslugcats/world to <ROOT_FP>/MSC, replacing any collisions.
ROOT_FP = "D:/RW files"

########################################################################################################################
re_room_settings_filename = re_rsf = re.compile(r'((\S+)_\S+)_settings(?:-(\S+))?\.txt')
# No point documenting every placedobject - whitelist the ones relevant for logic here.
OBJECT_WHITELIST = [
    # food quest
    "SlimeMold", "DangleFruit", "Mushroom", "WaterNut", "JellyFish", "GlowWeed", "Hazer", "LillyPuck",
    "DandelionPeach", "GooieDuck",
    # physical checks
    "BlueToken", "GreenToken", "RedToken", "GoldToken", "WhiteToken", "DevToken", "UniqueDataPearl",
    "KarmaFlower",  # artificer echo logic
    "SeedCob",  # for The Monk
    "BubbleGrass",  # for waterway traversal
    "VultureGrub", "DeadVultureGrub",  # expanded food quest
]
SHINY_LIST = ["BlueToken", "GreenToken", "RedToken", "GoldToken", "WhiteToken", "UniqueDataPearl", "DataPearl"]

########################################################################################################################
data = {}
# (root)
#   game version ("1.9.15.3" | "1.10.1")
#     dlcstate ("Vanilla" | "MSC")
#       region code
#         room name
#           "whitelist": set of whitelisted scugs
#           "blacklist": set of blacklisted scugs
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


########################################################################################################################
scugs_vanilla = {"Yellow", "White", "Red"}
scugs_msc = {"Yellow", "White", "Red", "Gourmand", "Artificer", "Rivulet", "Spear", "Saint", "Inv"}
scugs_watcher = {"Yellow", "White", "Red", "Watcher"}
scugs_msc_watcher = {"Yellow", "White", "Red", "Gourmand", "Artificer", "Rivulet", "Spear", "Saint", "Inv", "Watcher"}

scugs_by_gameversion = {
    "1.9.15.3": {"Vanilla": scugs_vanilla, "MSC": scugs_msc},
    "1.10.1": {"Vanilla": scugs_vanilla, "MSC": scugs_msc, "Watcher": scugs_watcher, "MSC_Watcher": scugs_msc_watcher}
}

########################################################################################################################
for gameversion, dlcstate_and_scugs in scugs_by_gameversion.items():
    gameversion_data = data.setdefault(gameversion, {})
    for dlcstate, all_scugs in dlcstate_and_scugs.items():
        gameversion_data[dlcstate] = {}

        # Loop over every world file.
        for fp in glob(path.join(ROOT_FP, gameversion, dlcstate, 'world', '*', 'world_*.txt')):
            region = path.basename(fp).split("_")[1].split(".")[0].upper()
            region_data = gameversion_data[dlcstate].setdefault(region, {})

            with open(fp) as f:
                # The world files are broken up into distinct blocks with clear entry and exit.
                block = None

                for line in f:
                    line = line.strip()

                    if line.startswith("ROOMS"):
                        block = "ROOMS"
                    elif line.startswith("END ROOMS"):
                        block = None
                    elif line.startswith("CONDITIONAL LINKS"):
                        block = "LINKS"
                    elif line.startswith("END CONDITIONAL LINKS"):
                        block = None
                    elif line.startswith("CREATURES"):
                        block = "CREATURES"
                    elif line.startswith("END CREATURES"):
                        block = None
                    # Comments are found in some world files.
                    elif block is None or line.startswith("//") or len(line) == 0:
                        continue

    ####################################################################################################################
                    elif block == "LINKS":
                        parts = splitstrip(line, ":")

                        # A room whitelist looks like `Spear : EXCLUSIVE_ROOM : GW_A07_PAST`.
                        # We force the room name to be uppercase for consistency;
                        # room names can't differ by capitalization alone anyway.
                        match parts:
                            case [scugname, "EXCLUSIVEROOM", roomname]:
                                sdc(region_data, {scugname}, roomname.upper(), "whitelist")

                            case [scugname, "HIDEROOM", roomname]:
                                sdc(region_data, {scugname}, roomname.upper(), "blacklist")

                            # A conditional room connection looks like `Artificer : GATE_HI_GW : GW_B01 : GW_B01_PAST`.
                            # We don't need these for the static data right now.
                            case [scugname, sourcename, old_destname, new_destname]:
                                pass

                            case _:
                                raise ValueError(f"Unrecognized conditional link: '{line}'")

    ####################################################################################################################
                    elif block == "ROOMS":
                        parts = splitstrip(line, ":")

                        # A room definition looks like `GW_A12 : GW_B04, GW_C07 : SCAVTRADER`.
                        # There can be (and often are) multiple connections, and there may not be a third part
                        # (room tags).
                        match parts:
                            case [roomname, connections, tags]:
                                sdc(region_data, {a.upper() for a in splitstrip(tags, ",")}, roomname.upper(), "tags")

                            case [roomname, connections]:
                                sdc(region_data, None, roomname.upper())

                            case _:
                                raise ValueError(f"Unrecognized room declaration: '{line}'")

    ####################################################################################################################
                    elif block == "CREATURES":
                        # Den declarations take several forms.
                        # First, they may be preceded by a scug whitelist or blacklist in parentheses.

                        scugstring = None
                        if line.startswith('('):
                            scugstring, line = line[1:].split(')', 1)

                        parts = line.split(" : ")

                        # A lineage den declaration looks like:
                        #   `LINEAGE : GW_B02 : 4 : White-0.3, BigSpider-0.3, SpitterSpider-0`
                        # Each entry is LINEAGE : {ROOM} : {DEN NUMBER} : {CREATURE TYPE}-{LINEAGE CHANCE}, repeat.
                        if parts[0] == "LINEAGE":
                            room, den_number, critstring = parts[1:]
                            spawner = Spawner(scugstring, room, den_number, critstring, True, dlcstate == "Vanilla")

                            for i, crit in enumerate(spawner.crits):
                                if crit.type != "NONE":
                                    dentype = "lineage_start" if i == 0 else ("lineage_end" if i == len(spawner.crits) - 1 else "lineage_mid")
                                    sdc(region_data, set(spawner.scugs), room.upper(), "spawners", dentype, crit.type)

                        # A normal den declaration looks like:
                        # GW_C02 : 2-CicadaB-2, 3-CicadaB, 5-Scavenger-{PreCycle,Seed:2837}, 5-TentaclePlant-{PreCycle}
                        # Each entry is {ROOM} : {DEN NUMBER}-{CREATURE TYPE}-{COUNT OR ATTRIBUTES, OPTIONAL}, repeat.
                        else:
                            room, critstrings = parts
                            for critstring in critstrings.split(', '):
                                den_number, critstring = critstring.split('-', 1)
                                spawner = Spawner(scugstring, room, den_number, critstring, False, dlcstate == "Vanilla")

                                for crit in spawner.crits:
                                    if crit.type != "NONE":
                                        dentype = "precycle" if "PreCycle" in crit.attributes else "normal"
                                        sdc(region_data, set(spawner.scugs), room.upper(), "spawners", dentype, crit.type)

    ####################################################################################################################
        # Get the set of all normal settings files to be subtracted from all settings files to get alt settings files.
        normal_settings_files = set(glob(path.join(ROOT_FP, gameversion, dlcstate, 'world', '??-rooms', '??_*_settings.txt')))
        all_settings_files = set(glob(path.join(ROOT_FP, gameversion, dlcstate, 'world', '??-rooms', '??_*_settings*')))

        # We need to process the normal settings files first, then update with alt settings files.
        for fp in list(normal_settings_files) + list(all_settings_files - normal_settings_files):
            if match := re_rsf.match(path.basename(fp)):
                room, region, scug = match.groups()
                # We force the room to be uppercase as in previous sections.
                room, region, scug = room.upper(), region.upper(), scug.title() if scug else None
            else:
                # There are some settings files with invalid names that won't be read by the game.
                continue

            try:
                room_data = gameversion_data[dlcstate][region][room]
            except KeyError:
                # If there isn't an entry for the room already, then it's not in a world file
                # and therefore not connected to the rest of the region - such as Artificer dream rooms in GW.
                continue

            # Temporary dicts to hold information from this settings file.
            room_objects = parse_placed_objects(fp)
            r_data = {'shinies': {}, 'objects': {}}

            for obj in room_objects:
                custom_data = obj["data"]
                blacklist: set = obj["filtered"]

                if obj['type'] in SHINY_LIST:
                    # For shinies, we need the name.
                    name = custom_data[4 if "Pearl" in obj['type'] else 5]
                    # Tokens have their own blacklist in custom data, though it's not always used.
                    if "Token" in obj['type']:
                        blacklist = set(custom_data[6].split("|")).union(blacklist or set())
                    # Pearls with `Misc` in the name or a blank name should be ignored.
                    elif "Misc" in name or name.strip() == "":
                        continue

                    r_data["shinies"][name] = {"filter": blacklist, "kind": obj["type"]}

                elif obj['type'] in OBJECT_WHITELIST:
                    try:
                        # If this object already has an entry in the temp data,
                        # then there's another placed object of the same kind.
                        # Add in the new blacklist (which is an intersection).
                        s = r_data['objects'][obj['type']]['filter']
                        r_data['objects'][obj['type']]['filter'] = s.intersection(blacklist or set())
                    except KeyError:
                        r_data['objects'][obj['type']] = {"filter": blacklist or set()}

    ####################################################################################################################
            if scug is None:
                # This is normal settings file; just directly update the room data.
                room_data.update(r_data)
            else:
                # This is an alt settings file.  First, add this scug to the list of alted scugs.
                sdc(room_data, {scug}, "alted")

                for shiny_name, shiny_data in r_data['shinies'].items():
                    # On the rare off-chance that an alt settings file blacklist the scug in question.
                    if scug not in shiny_data["filter"]:
                        # Update the room data - importantly updating the whitelist
                        sdc(room_data, shiny_data["kind"], "shinies", shiny_name, "kind")
                        sdc(room_data, {scug}, "shinies", shiny_name, "whitelist")

                for object_name, object_data in r_data['objects'].items():
                    if scug not in object_data["filter"]:
                        sdc(room_data, {scug}, "objects", object_name, "whitelist")

    ####################################################################################################################
        # Append region code to gate names (there are at least two version of every gate room).
        # Yes, they're stored under different region dicts, but this simplifies the AP connection logic.
        for region, region_data in gameversion_data[dlcstate].items():
            gates = {k: v for k, v in region_data.items() if "GATE" in v.get("tags", ())}
            region_data.update({f'{k}[{region}]': v for k, v in gates.items()})

            for key in gates.keys():
                del region_data[key]

########################################################################################################################

with open("data.py", "w") as f:
    f.write(f'data = {data}\n')

print('script ending normally')
