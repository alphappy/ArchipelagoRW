from typing import Iterable


class GameStateFlag:
    """Encapsulates a set of gamestates with a bitflag."""
    value: int

    def __init__(self, vanilla: Iterable[str] | int | None = None,
                 msc: Iterable[str] | None = None, whitelist: bool = False):
        """
        :param vanilla:  A set of vanilla scug IDs.  Alternatively, an integer which sets the entire flag.
        :param msc:  A set of MSC scug IDs.  Ignored if `vanilla` is an integer.
        :param whitelist:
        If `True`, `vanilla` and `msc` specify whitelists and all other gamestates default to excluded.
        If `False`, `vanilla` and `msc` specify blacklists and all other gamestates default to included.
        Ignored if `vanilla` is an integer.
        """
        if type(vanilla) == int:
            self.value = vanilla
        else:
            self.value = 0 if whitelist else 0b111_111_111_111
            if vanilla is not None:
                self.set_scugs("Vanilla", vanilla, whitelist)
            if msc is not None:
                self.set_scugs("MSC", msc, whitelist)

    _scug_masks: dict[str, dict[str, int]] = {
        "Vanilla": {s: 1 << i for i, s in enumerate(('Yellow', 'White', 'Red'))},
        "MSC": {s: 1 << (i+3) for i, s in enumerate(
            ('Yellow', 'White', 'Red', 'Gourmand', 'Artificer', 'Rivulet', 'Spear', 'Saint', 'Inv')
        )}
    }

    _dlcstate_masks: dict[str, int] = {"Vanilla": 0b111, "MSC": 0b111_111_111_000}

    @staticmethod
    def _get_mask(dlcstate: str, scug: str | None = None) -> int:
        if scug is None:
            return GameStateFlag._dlcstate_masks[dlcstate]
        return GameStateFlag._scug_masks[dlcstate][scug]

    def set_scugs(self, dlcstate: str, scugs: Iterable[str], value: bool) -> None:
        """Set the bits corresponding to the gamestate with `dlcstate` and `scugs` to `value`."""
        self._set_mask(sum(self._get_mask(dlcstate, scug) for scug in set(scugs)), value)

    def set_dlcstate(self, dlcstate: str, value: bool) -> None:
        """Set all the bits for `dlcstate` to `value`."""
        self._set_mask(self._get_mask(dlcstate), value)

    def _set_mask(self, mask: int, value: bool) -> None:
        if value:
            self.value |= mask
        else:
            self.value = ~(~self.value | mask)

    def get(self, dlcstate: str, scug: str) -> bool:
        return self.value & (self._get_mask(dlcstate, scug)) != 0

    def __getitem__(self, item: tuple[str, str]) -> bool:
        return self.get(item[0], item[1])

    def __setitem__(self, key: str | tuple[str, str] | tuple[str, Iterable[str]], value: bool) -> None:
        if type(key) == str:
            self.set_dlcstate(key, value)
        else:
            dlcstate, scugs = key
            self.set_scugs(dlcstate, {scugs} if type(scugs) == str else scugs, value)

    def __repr__(self) -> str:
        return f"GameStateFlag(0b{self.value:b})"
