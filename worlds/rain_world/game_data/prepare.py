from os.path import join, exists
from os import remove
from shutil import copytree


# Path to `Rain World` folder containing `RainWorld_Data`.
RW_FOLDER = r'C:\Program Files (x86)\Steam\steamapps\common\Rain World'
# Path to folder which will contain RW files.
OUTPUT_FOLDER = 'D:/RW files'

REGRAB_VANILLA = True


def ignore(path: str, items: list[str]) -> list[str]:
    rooms_folders = {i for i in items if i.endswith("-rooms")}
    world_folders = {i[:-6] for i in rooms_folders}

    world_files = {i for i in items if (i.startswith("world_") or i.startswith("properties") or "_settings" in i) and i.endswith(".txt")}

    return list(set(items).difference(rooms_folders).difference(world_folders).difference(world_files))


sa_folder = join(RW_FOLDER, "RainWorld_Data", "StreamingAssets")
version = open(join(sa_folder, "GameVersion.txt")).read().replace("v", "").strip()
prompt = """Start Rain World with desired combination of mods, reload it, and wait for it to reach the main menu.
Then, enter the name of the current modstate (or leave blank to exit):   """

if REGRAB_VANILLA or not exists(join(OUTPUT_FOLDER, version, "Vanilla")):
    dst = join(OUTPUT_FOLDER, version, "Vanilla", "world")
    copytree(join(sa_folder, "world"), dst, ignore=ignore, dirs_exist_ok=True)
    remove(join(dst, "su", "world_su - copy.txt"))
    remove(join(dst, "gw-rooms", "world_gw.txt"))

while (modstate := input(prompt)) != "":
    dst = join(OUTPUT_FOLDER, version, modstate, "world")
    copytree(join(OUTPUT_FOLDER, version, "Vanilla", "world"), dst, dirs_exist_ok=True)
    if "MSC" in modstate:
        copytree(join(sa_folder, "mods", "moreslugcats", "world"), dst, ignore=ignore, dirs_exist_ok=True)
    if "Watcher" in modstate:
        copytree(join(sa_folder, "mods", "watcher", "world"), dst, ignore=ignore, dirs_exist_ok=True)
    copytree(join(sa_folder, "mergedmods", "world"), dst, dirs_exist_ok=True)


print('script ending normally')
