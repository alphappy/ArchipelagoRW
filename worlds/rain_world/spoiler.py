import logging
from typing import List, Optional, Set, Dict

from BaseClasses import Spoiler, CollectionState, Location, Item


def get_collection_spheres(self: Spoiler) -> list[set[Location]]:
    """Destructive to the multiworld while it is run, damage gets repaired afterwards."""
    from itertools import chain
    # get locations containing progress items
    multiworld = self.multiworld
    prog_locations = {location for location in multiworld.get_filled_locations() if location.item.advancement}
    state_cache: List[Optional[CollectionState]] = [None]
    collection_spheres: List[Set[Location]] = []
    state = CollectionState(multiworld)
    sphere_candidates = set(prog_locations)
    logging.debug('Building up collection spheres.')
    while sphere_candidates:

        # build up spheres of collection radius.
        # Everything in each sphere is independent from each other in dependencies and only depends on lower spheres

        sphere = {location for location in sphere_candidates if state.can_reach(location)}

        for location in sphere:
            state.collect(location.item, True, location)

        sphere_candidates -= sphere
        collection_spheres.append(sphere)
        state_cache.append(state.copy())

        logging.debug('Calculated sphere %i, containing %i of %i progress items.', len(collection_spheres),
                      len(sphere),
                      len(prog_locations))
        if not sphere:
            logging.debug('The following items could not be reached: %s', ['%s (Player %d) at %s (Player %d)' % (
                location.item.name, location.item.player, location.name, location.player) for location in
                                                                           sphere_candidates])
            if any([multiworld.worlds[location.item.player].options.accessibility != 'minimal' for location in
                    sphere_candidates]):
                raise RuntimeError(f'Not all progression items reachable ({sphere_candidates}). '
                                   f'Something went terribly wrong here.')
            else:
                self.unreachables = sphere_candidates
                break

    # in the second phase, we cull each sphere such that the game is still beatable,
    # reducing each range of influence to the bare minimum required inside it
    restore_later: Dict[Location, Item] = {}
    for num, sphere in reversed(tuple(enumerate(collection_spheres))):
        to_delete: Set[Location] = set()
        for location in sphere:
            # we remove the item at location and check if game is still beatable
            logging.debug('Checking if %s (Player %d) is required to beat the game.', location.item.name,
                          location.item.player)
            old_item = location.item
            location.item = None
            if multiworld.can_beat_game(state_cache[num]):
                to_delete.add(location)
                restore_later[location] = old_item
            else:
                # still required, got to keep it around
                location.item = old_item

        # cull entries in spheres for spoiler walkthrough at end
        sphere -= to_delete

    # second phase, sphere 0
    removed_precollected: List[Item] = []

    for precollected_items in multiworld.precollected_items.values():
        # The list of items is mutated by removing one item at a time to determine if each item is required to beat
        # the game, and re-adding that item if it was required, so a copy needs to be made before iterating.
        for item in precollected_items.copy():
            if not item.advancement:
                continue
            logging.debug('Checking if %s (Player %d) is required to beat the game.', item.name, item.player)
            precollected_items.remove(item)
            multiworld.state.remove(item)
            if not multiworld.can_beat_game():
                # Add the item back into `precollected_items` and collect it into `multiworld.state`.
                multiworld.push_precollected(item)
            else:
                removed_precollected.append(item)

    # we are now down to just the required progress items in collection_spheres. Unfortunately
    # the previous pruning stage could potentially have made certain items dependant on others
    # in the same or later sphere (because the location had 2 ways to access but the item originally
    # used to access it was deemed not required.) So we need to do one final sphere collection pass
    # to build up the correct spheres

    required_locations = {item for sphere in collection_spheres for item in sphere}
    state = CollectionState(multiworld)
    collection_spheres = []
    while required_locations:
        sphere = set(filter(state.can_reach, required_locations))

        for location in sphere:
            state.collect(location.item, True, location)

        collection_spheres.append(sphere)

        logging.debug('Calculated final sphere %i, containing %i of %i progress items.', len(collection_spheres),
                      len(sphere), len(required_locations))

        required_locations -= sphere
        if not sphere:
            raise RuntimeError(f'Not all required items reachable. Unreachable locations: {required_locations}')

    # repair the multiworld again
    for location, item in restore_later.items():
        location.item = item

    for item in removed_precollected:
        multiworld.push_precollected(item)

    return collection_spheres

