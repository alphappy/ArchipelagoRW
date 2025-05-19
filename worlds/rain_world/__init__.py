__all__ = ["RainWorldWorld", "RainWorldWebWorld"]

from typing import Mapping, Any

from Options import OptionError
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, LocationProgressType
from .game_data.shelters import get_starts, ingame_capitalization, get_default_start
from .options import RainWorldOptions
from .conditions.classes import Simple
from .game_data.general import region_code_to_name, story_regions, passage_proper_names
from .events import get_events
from .regions.classes import room_to_region
from .regions.gates import gates
from .utils import normalize, flounder2
from .items import RainWorldItem, all_items, RainWorldItemData, portal_keys
from . import regions, locations, options
from .game_data.general import prioritizable_passages, passages_all, passages_vanilla, accessible_gates


class RainWorldWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Rain World for Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["alphappy"]
    )]
    option_groups = options.option_groups
    rich_text_options_doc = True
    theme = "ocean"
    bug_report_page = "https://github.com/alphappy/ArchipelagoRW/issues"


class RainWorldWorld(World):
    """You are a nomadic slugcat, both predator and prey in a broken ecosystem. Grab your spear and brave the
    industrial wastes, hunting enough food to survive, but be wary— other, bigger creatures have the same plan...
    and slugcats look delicious."""
    game = "Rain World"  # name of the game/world
    options_dataclass = RainWorldOptions  # options the player can set
    options: RainWorldOptions  # typing hints for option results
    topology_present = True  # show path to required location checks in spoiler
    web = RainWorldWebWorld()

    item_name_to_id = items.item_name_to_id
    location_name_to_id = locations.classes.location_map

    item_name_groups = items.item_hints
    location_name_groups = locations.classes.location_hints

    location_count = 0
    starting_room = 'SU_C04'
    start_is_default = True
    start_is_connected = False
    foodquest_accessibility_flag = 0
    predetermined_warps = {}

    def generate_early(self) -> None:
        # This is the earliest that the options are available.  Player YAML failures should be tripped here.

        if (gamestate_error := self.options.check_gamestate_validity()) is not None:
            raise OptionError(f"Invalid YAML for {self.player_name}: {gamestate_error}")

        #################################################################
        # STARTING REGION
        self.starting_room = self.random.choice(get_starts(self.options))
        self.start_is_default = self.options.random_starting_region == 0

    def create_regions(self):
        for data in regions.generate(self.options, self.random):
            data.make(self.player, self.multiworld, self.options)

        # return for each datum is a bool for whether that location was actually generated
        locs = [data.make(self.player, self.multiworld, self.options) for data in locations.generate(self.options)]
        foodquest_locs = [
            data.make(self.player, self.multiworld, self.options) for data in locations.generate_foodquest(self.options)
        ]
        self.location_count = sum(locs + foodquest_locs)
        self.foodquest_accessibility_flag = sum(e << i for i, e in enumerate(foodquest_locs))

        for data in get_events(self.options, self.multiworld.get_regions(self.player)):
            data.make(self.player, self.multiworld, self.options)

        #################################################################
        # PRIORITY PASSAGES
        if num := self.options.passage_priority.value > 0:
            unprioritized_passage_locations = [
                l for l in self.multiworld.get_locations(self.player)
                if l.name.startswith("Passage-") and l.progress_type == LocationProgressType.DEFAULT
            ]
            for loc in self.random.sample(unprioritized_passage_locations,
                                          min([num, len(unprioritized_passage_locations)])):
                loc.progress_type = LocationProgressType.PRIORITY

        #################################################################
        # STARTING REGION - defer this step for UT.
        if not hasattr(self.multiworld, "generation_is_fake"):
            self.connect_starting_region(self.starting_room)

    def connect_starting_region(self, room: str):
        if not self.start_is_connected:
            if room == "":
                room = get_default_start(self.options.starting_scug)
            start = self.multiworld.get_region(room_to_region[room], self.player)
            self.multiworld.get_region('Menu', self.player).connect(start, "Starting region")
            self.start_is_connected = True

    def create_item(self, name: str) -> RainWorldItem:
        return items.all_items[name].generate_item(self.player)

    def create_items(self) -> None:
        added_items = 0

        if self.options.starting_scug != "Watcher":
            pool = {
                "Karma": 8 + self.options.extra_karma_cap_increases.value,
                **{gate.names[0]: 1 for gate in (
                    [g for g in gates if g.is_accessible(self.options)]
                    if self.options.which_gate_behavior != "karma_only" else []
                )},
                **{f"Passage Token - {passage_proper_names[p]}": 1
                   for p in (passages_all if self.options.msc_enabled else passages_vanilla)},
                "The Mark": 1,
                "The Glow": 1,
                "Slag Key": 1 if self.options.starting_scug == "Red" else 0,
                "Citizen ID Drone": 1 if self.options.starting_scug == "Artificer" else 0,
                "Longer cycles": 1 if self.options.starting_scug == "Rivulet" else 0,
                "Rarefaction Cell": 1 if self.options.starting_scug == "Rivulet" else 0,
                "Moon's Final Message": 1 if self.options.starting_scug == "Spear" else 0,
                "Spearmaster's Pearl": 1 if self.options.starting_scug == "Spear" else 0,
            }
        else:
            pool = {
                "Ripple": 12 + self.options.extra_karma_cap_increases.value,
                **{k: 1 for k in portal_keys.keys()},
            }

        precollect = {
            "MSC": 1 if self.options.msc_enabled else 0,
            f"Scug-{self.options.starting_scug}": 1,
            "Option-Glow": 0 if self.options.difficulty_glow else 1,
        }

        for name, count in pool.items():
            for i in range(count):
                self.multiworld.itempool.append(self.create_item(name))
            added_items += count

        for name, count in precollect.items():
            for i in range(count):
                self.multiworld.push_precollected(self.create_item(name))

        #################################################################
        # FILLER POPULATION
        remaining_slots = self.location_count - added_items
        trap_fraction = self.options.pct_traps / 100

        nontrap_weights = normalize(self.jitter(self.options.get_nontrap_weight_dict()))
        trap_weights = normalize(self.jitter(self.options.get_trap_weight_dict()))

        d: dict[str, float] = {}
        d.update({k: v * (1 - trap_fraction) for k, v in nontrap_weights.items()})
        d.update({k: v * trap_fraction for k, v in trap_weights.items()})

        self.multiworld.itempool += [self.create_item(e) for e in flounder2(d, remaining_slots)]

    def jitter(self, d: dict[Any, float]) -> dict[Any, float]:
        return {k: 0 if v == 0 else (v + self.random.random() * self.options.weight_jitter) for k, v in d.items()}

    def set_rules(self) -> None:
        # ascension_item = Item("Ascension", ItemClassification.progression, None, self.player)
        # self.multiworld.get_location("Ascension", self.player).place_locked_item(ascension_item)
        self.multiworld.completion_condition[self.player] = Simple("Victory").check(self.player)

    def fill_slot_data(self) -> Mapping[str, Any]:
        d = self.options.as_dict(
            # Plugin needs to know...
            "which_game_version",  # ...which game version should be used.
            "is_msc_enabled",  # ...whether MSC should be enabled.
            "is_watcher_enabled",  # ...whether The Watcher should be enabled.
            "which_campaign",  # ...which campaign should be selected.
            "passage_progress_without_survivor",  # ...if this setting doesn't match Remix.
            "death_link",  # ...whether to listen for death link notifications.
            "checks_foodquest",  # ...whether the food quest should be available.
            "checks_broadcasts",  # ...whether broadcasts should be avilable.
            "checks_tokens_pearls",  # ...whether all tokens should be available.
            "checks_sheltersanity",  # ...whether sheltersanity is enabled.
            "which_victory_condition",  # ...which victory condition is a win.
            "which_gate_behavior",  # ...how gates should behave.
            "difficulty_echo_low_karma",  # ...how low-karma echo appearances should be handled.
        )
        # backwards compatibility
        d["which_gamestate"] = self.options.which_gamestate_integer
        # ...which room to spawn in.  Empty string for default.
        d["starting_room"] = ("" if self.start_is_default
                              else ingame_capitalization.get(self.starting_room, self.starting_room))
        # ...which food quest checks are accessible.
        d["checks_foodquest_accessibility"] = (
            self.foodquest_accessibility_flag if self.options.checks_foodquest_expanded else 0)

        if self.predetermined_warps:
            d["predetermined_warps"] = self.predetermined_warps

        return d

    # def generate_output(self, output_directory: str) -> None:
    #     import json
    #     with open(f'{output_directory}/client_map.json', 'w') as f:
    #         json.dump({"locations": locations.classes.location_client_map, "items": items.item_client_names}, f)

    def interpret_slot_data(self, slot_data: dict[str, Any]) -> None:
        """Universal Tracker support - synchronize UT internal multiworld with actual slot data."""
        self.connect_starting_region(slot_data["starting_room"].upper())
