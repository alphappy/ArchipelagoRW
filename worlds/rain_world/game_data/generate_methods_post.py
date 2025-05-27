from .bitflag import ScugFlag


def recursive_flag_expansion(d: dict, force_all: bool = False, to_set: bool = True):
    for k, v in d.items():
        if force_all or (k in ("alted", "filter", "whitelist", "blacklist", "broken") and type(v) == int):
            d[k] = ScugFlag(v).get_all_primary_flags() if to_set else ScugFlag(v)
        elif k == "spawners":
            for k2, v2 in v.items():
                recursive_flag_expansion(v2, True)
        elif type(v) == dict:
            recursive_flag_expansion(v)
