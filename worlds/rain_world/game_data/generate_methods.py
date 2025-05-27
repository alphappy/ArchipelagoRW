import re

from bitflag import ScugFlag

re_3 = re.compile(r'\b(\w+)><([\d.]+)><([\d.]+)><([^,]*)')


def parse_placed_objects(fp: str) -> list[dict]:
    """Open `fp`, a room settings file, and parse its PlacedObjects.  Filter objects are applied."""
    room_objects = []
    filter_objects = []
    with open(fp, 'r') as file:
        for line in file:
            if line.startswith('PlacedObjects:'):
                for objnum, (objtype, x, y, objdata) in enumerate(re_3.findall(line)):
                    (filter_objects if objtype == "Filter" else room_objects).append(
                        dict(type=objtype, x=float(x), y=float(y), data=objdata.split('~'), filtered=None)
                    )

    for filter_obj in filter_objects:
        radius = (float(filter_obj['data'][0]) ** 2 + float(filter_obj['data'][1]) ** 2) ** 0.5
        for obj in room_objects:
            if obj['filtered'] is None:
                dist = ((filter_obj['x'] - obj['x']) ** 2 + (filter_obj['y'] - obj['y']) ** 2) ** 0.5
                if dist <= radius:
                    obj['filtered'] = set(filter_obj["data"][-1].split('|'))

    for room_obj in room_objects:
        room_obj['filtered'] = room_obj['filtered'] or set()

    return room_objects


def setdefaultchain(root: dict, value, *keys):
    """
    Starting with a root dictionary, access a sequence of keys, ensuring that dictionaries exist at each step,
    then set a value.
    :param root:  The root dictionary.
    :param value:  The value to set.
    If `None`, the no value is set; this just ensures that each dict in the chain exists.
    If a set or list, and the value already at the target is the same, they are combined.
    :param keys:  The sequence of keys to access.
    :return:  None
    """
    d = root
    for key in (keys if value is None else keys[:-1]):
        d = d.setdefault(key, {})

    if value is None:
        return

    try:
        existing = d[keys[-1]]

        if type(value) == set and type(existing) == set:
            d[keys[-1]].update(value)
        elif type(value) == list and type(existing) == list:
            d[keys[-1]].extend(value)
        else:
            d[keys[-1]] = value

    except KeyError:
        d[keys[-1]] = value


def splitstrip(text: str, *args) -> list[str]:
    """Split a string, then strip() each element of the array."""
    return [i.strip() for i in text.split(*args)]


def recursive_flag_reduction(d: dict):
    for k, v in d.items():
        if type(v) == ScugFlag:
            d[k] = v.value
        elif type(v) == dict:
            recursive_flag_reduction(v)
