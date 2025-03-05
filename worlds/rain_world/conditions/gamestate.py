from typing import Iterable


class GameStateFlag:
    """Encapsulates a set of gamestates with a bitflag."""
    value: int

    def __init__(self, vanilla: Iterable[str] | int | None = None,
                 msc: Iterable[str] | None = None, whitelist: bool = False):
        if type(vanilla) == int:
            self.value = vanilla
        else:
            self.value = 0 if whitelist else 0b111_111_111_111
            if vanilla is not None:
                self.set_scugs("Vanilla", vanilla, whitelist)
            if msc is not None:
                self.set_scugs("MSC", msc, whitelist)

    _scug_masks = {
        "Vanilla": {s: 1 << i for i, s in enumerate(('Yellow', 'White', 'Red'))},
        "MSC": {s: 1 << (i+3) for i, s in enumerate(
            ('Yellow', 'White', 'Red', 'Gourmand', 'Artificer', 'Rivulet', 'Spear', 'Saint', 'Inv')
        )}
    }

    _dlcstate_masks = {"Vanilla": 0b111, "MSC": 0b111_111_111_000}

    @staticmethod
    def _get_mask(dlcstate: str, scug: str | None = None):
        if scug is None:
            return GameStateFlag._dlcstate_masks[dlcstate]
        return GameStateFlag._scug_masks[dlcstate][scug]

    def set_scugs(self, dlcstate: str, scugs: Iterable[str], value: bool):
        self._set_mask(sum(self._get_mask(dlcstate, scug) for scug in set(scugs)), value)

    def set_dlcstate(self, dlcstate: str, value: bool):
        self._set_mask(self._get_mask(dlcstate), value)

    def _set_mask(self, mask: int, value: bool):
        if value:
            self.value |= mask
        else:
            self.value = ~(~self.value | mask)

    def get(self, dlcstate: str, scug: str): return self.value & (self._get_mask(dlcstate, scug)) != 0

    def __getitem__(self, item: tuple[str, str]): return self.get(item[0], item[1])

    def __setitem__(self, key: str | tuple[str, str] | tuple[str, Iterable[str]], value: bool):
        if type(key) == str:
            self.set_dlcstate(key, value)
        else:
            dlcstate, scugs = key
            self.set_scugs(dlcstate, {scugs} if type(scugs) == str else scugs, value)

    def __repr__(self): return f"GameStateFlag(0b{self.value:b})"
