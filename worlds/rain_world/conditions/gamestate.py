from typing import Iterable


class GameStateFlag:
    """Encapsulates a set of gamestates with a bitflag."""

    value: int
    def __init__(self, vanilla: Iterable[str] | int | None = None,
                 msc: Iterable[str] | None = None, whitelist: bool = False):
        if type(vanilla) == int:
            self.value = vanilla
        elif whitelist:
            self.value = 0
            if vanilla is not None:
                self.set_scugs("Vanilla", vanilla, True)
            if msc is not None:
                self.set_scugs("MSC", msc, True)
        else:
            self.value = 0b111_111_111_111
            if vanilla is not None:
                self.set_scugs("Vanilla", vanilla, False)
            if msc is not None:
                self.set_scugs("MSC", msc, False)

    _index = {
        "Vanilla": {s: i for i, s in enumerate(('Yellow', 'White', 'Red'))},
        "MSC": {s: i+3 for i, s in enumerate(
            ('Yellow', 'White', 'Red', 'Gourmand', 'Artificer', 'Rivulet', 'Spear', 'Saint', 'Inv')
        )}
    }

    _dlcstate_mask = {"Vanilla": 0b111, "MSC": 0b111_111_111_000}

    @staticmethod
    def bit(dlcstate: str, scug: str): return GameStateFlag._index[dlcstate][scug]

    def set_scugs(self, dlcstate: str, scugs: Iterable[str], value: bool):
        self.set_mask(sum(1 << GameStateFlag.bit(dlcstate, scug) for scug in set(scugs)), value)

    def set_dlcstate(self, dlcstate: str, value: bool):
        self.set_mask(GameStateFlag._dlcstate_mask[dlcstate], value)

    def set_mask(self, mask: int, value: bool):
        if value:
            self.value |= mask
        else:
            self.value = ~(~self.value | mask)

    def get(self, dlcstate: str, scug: str): return self.value & (1 << GameStateFlag.bit(dlcstate, scug)) != 0

    def __getitem__(self, item: tuple[str, str]): return self.get(item[0], item[1])

    def __setitem__(self, key: str | tuple[str, str] | tuple[str, Iterable[str]], value: bool):
        if type(key) == str:
            self.set_dlcstate(key, value)
        else:
            dlcstate, scugs = key
            self.set_scugs(dlcstate, {scugs} if type(scugs) == str else scugs, value)

    def __repr__(self): return f"GameStateFlag(0b{self.value:b})"
