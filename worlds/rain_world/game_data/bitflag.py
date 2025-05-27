# THIS SCRIPT MUST NOT IMPORT!


def named_bit_flag(class_name: str, primary_names: list[str], secondary_names: dict[str, set[int]] | None = None):
    bitmap: dict[str, int] = {
        **{name: 1 << i for i, name in enumerate(primary_names)},
        **{name: sum(1 << i for i in bits) for name, bits in (secondary_names or {}).items()}
    }
    bitlength = len(primary_names)

    class NamedBitFlag:
        """Encapsulates a bitflag with named bits."""
        value: int

        def __init__(self, value: int | set[str] = 0, inverted: bool = False):
            self.bitlength = bitlength
            self.value = value if type(value) == int else 0
            if type(value) == set:
                if inverted:
                    self._set_all(True)
                self._set_flags(value, not inverted)

        def _set_mask(self, mask: int, on: bool) -> None: self.value = (self.value | mask) if on else ~(~self.value | mask)
        def _set_bits(self, bits: set[int], on: bool) -> None: self._set_mask(sum(1 << i for i in bits), on)
        def _set_bit(self, bit: int, on: bool) -> None: self._set_mask(1 << bit, on)
        def _set_flags(self, flags: set[str], on: bool) -> None: self._set_mask(self._mask_from_flags(flags), on)
        def _set_all(self, on: bool) -> None: self._set_bits(set(range(bitlength)), on)

        def _get_mask(self, mask: int) -> bool: return self.value & mask != 0
        def _get_bit(self, bit: int) -> bool: return (self.value & (1 >> bit)) != 0
        def _get_flag(self, flag: str) -> bool: return self._get_mask(self._mask_from_flags({flag}))

        @staticmethod
        def _mask_from_flags(flags: set[str]) -> int: return sum(bitmap[flag] for flag in flags)

        def get_all_primary_flags(self) -> set[str]: return {n for n in primary_names if self._get_flag(n)}
        def add(self, flag: str | set[str]): self._set_flags({flag} if type(flag) == str else flag, True)
        def remove(self, flag: str | set[str]): self._set_flags({flag} if type(flag) == str else flag, False)
        def intersect(self, flags: str | set[str]): self.value &= self._mask_from_flags(flags)

        def __getitem__(self, item: int | str) -> bool:
            return self._get_bit(item) if type(item) == int else self._get_flag(item)

        def __setitem__(self, key: int | str | tuple[str], value: bool) -> None:
            if type(key) == int:
                self._set_bit(key, value)
            elif type(key) == str:
                self._set_flags({key}, value)
            elif type(key) == tuple:
                self._set_flags(set(key), value)

        def __contains__(self, item): return self._get_flag(item)

        def __repr__(self) -> str:
            return f"{class_name}(0b{self.value:0>{self.bitlength}b})"

        def __eq__(self, other): return self.value == other.value
        def __ne__(self, other): return self.value != other.value

    return NamedBitFlag


ScugFlag = named_bit_flag(
    "ScugFlag",
    ["Yellow", "White", "Red", "Gourmand", "Artificer", "Rivulet", "Spear", "Saint", "Inv", "Watcher"],
    {"Vanilla": {0, 1, 2}, "MSC": {3, 4, 5, 6, 7, 8}}
)
