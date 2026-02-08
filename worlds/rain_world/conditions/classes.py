from typing import Callable, Optional

from BaseClasses import CollectionState
from rule_builder.rules import Rule, True_, False_, Or, And, CanReachLocation, HasFromList, HasFromListUnique


class Condition:
    # def check(self, player: int) -> Callable[[CollectionState], bool]:
    #     return lambda state: True

    def get_rule(self) -> Rule:
        return True_()


class Simple(Condition):
    def __init__(self, items: list[str] | set[str] | str, count: Optional[int] = None,
                 unique: Optional[bool] = None, locations: bool = False):
        """
        Represents a simple check against a CollectionState.  There are several ways the arguments may be specified.

        Check for at least 1 `"A"`:
         - `Simple("A")`
         - `Simple("A", 1)`

         Check for at least 5 `"A"`:
         - `Simple("A", 5)`

         Check for `"A"`, `"B"`, and `"C"`:
         - `Simple(["A", "B", "C"])`
         - `Simple(["A", "B", "C"], 3)`

         Check for any 2 of `"A"`, `"B"`, and `"C"`, ignoring duplicates (so `["A", "A"]` would not pass):
         - `Simple(["A", "B", "C"], 2)`

         Check for any 2 of `"A"`, `"B"`, and `"C"`, allowing duplicates (so `["A", "A"]` would pass):
         - `Simple(["A", "B", "C"], 2, unique=False)`

        :param items:  The item or list of items to check against.
        :param count:  The number of items that must be found in the CollectionState.
        If unspecified, all items must be found (`count == len(items)` if `items` is a list, or 1 otherwise).
        :param unique:  Whether duplicate items should be ignored.
        If unspecified, `unqiue` is `False` if `items` is a string and `True` if it's a list.
        :param locations:  Whether to treat `items` as a list of locations to check for access to
        rather than as a list of collected items.
        """
        self.unique: bool = unique or (type(items) == list) or (type(items) == set)
        self.items: list[str] = [items] if type(items) == str else items
        self.count: int = count or len(self.items)
        self.locations: bool = locations

    # def check(self, player: int) -> Callable[[CollectionState], bool]:
    #     def inner(state: CollectionState) -> bool:
    #         if len(self.items) == 0:
    #             return True
    #         if self.locations:
    #             ret = sum(state.can_reach_location(item, player) for item in self.items) >= self.count
    #         elif self.unique:
    #             ret = state.has_from_list_unique(self.items, player, self.count)
    #         else:
    #             ret = state.has_from_list(self.items, player, self.count)
    #
    #         return ret
    #     return inner

    def get_rule(self) -> Rule:
        if len(self.items) == 0:
            return True_()
        if self.locations:
            # Due to RuleBuilder restriction, you can only check for any or all locations.
            # No defined rules currently try to do any more than that,
            # so this simplification works until this is no longer the case.
            # TODO Allow checking for k of n locations satisfied
            if self.count == 1:
                return Or(*(CanReachLocation(item) for item in self.items))
            else:
                return And(*(CanReachLocation(item) for item in self.items))
        elif self.unique:
            return HasFromListUnique(*self.items, count=self.count)
        else:
            return HasFromList(*self.items, count=self.count)


class Compound(Condition):
    """Represents multiple checks against a CollectionState, some specified number of which must be satsified."""
    def __init__(self, count: int, *conditions: Condition):
        self.conditions = conditions
        self.count = count

    # def check(self, player: int) -> Callable[[CollectionState], bool]:
    #     def inner(state: CollectionState) -> bool:
    #         if self.count > len(self.conditions):
    #             return False
    #         elif self.count == len(self.conditions):
    #             return all(c.check(player)(state) for c in self.conditions)
    #         elif self.count == 1:
    #             return any(c.check(player)(state) for c in self.conditions)
    #         else:
    #             return sum(c.check(player)(state) for c in self.conditions) >= self.count
    #     return inner

    def get_rule(self) -> Rule:
        if self.count > len(self.conditions):
            return False_()
        elif self.count == len(self.conditions):
            return And(*(cond.get_rule() for cond in self.conditions))
        else: #self.count == 1:
            return Or(*(cond.get_rule() for cond in self.conditions))
        # Due to RuleBuilder restriction, you can only check for any or all Rules.
        # No defined rules currently try to do any more than that,
        # so this simplification works until this is no longer the case.
        # else:
        #     pass TODO Allow checking for k of n rules satisfied


class AnyOf(Compound):
    """Represents multiple checks against a CollectionState, at least one of which must be satsified."""
    def __init__(self, *conditions: Condition):
        super().__init__(1, *conditions)


class AllOf(Compound):
    """Represents multiple checks against a CollectionState, all of which must be satsified."""
    def __init__(self, *conditions: Condition):
        super().__init__(len(conditions), *conditions)


# The default "condition" which is always satisfied.
ConditionBlank = Condition()