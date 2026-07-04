__all__ = ["RainWorldWorld", "RainWorldWebWorld"]

from typing import Mapping, Any, TextIO

from Options import OptionError
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, LocationProgressType
from .game_data.shelters import get_starts, ingame_capitalization, get_default_start
from .game_data.watcher import normal_regions
from .options import RainWorldOptions
from .conditions.classes import Simple
from .game_data.general import region_code_to_name, all_regions, passage_proper_names
from .events import get_events
from .regions.classes import room_to_region
from .regions.gates import gates
from .utils import normalize, flounder2
from .items import RainWorldItem, portal_keys, PortalKeyItemData
from . import regions, locations, options, items
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

    ut_can_gen_without_yaml = True

    def generate_early(self) -> None:
        # This is the earliest that the options are available.  Player YAML failures should be tripped here.

        if (gamestate_error := self.options.general_validity_check()) is not None:
            raise OptionError(f"Invalid YAML for {self.player_name}: {gamestate_error}")

        #################################################################
        # STARTING REGION
        self.options.find_starting_region(self.random)
        self.starting_room = self.random.choice(get_starts(self.options))
        self.start_is_default = (self.options.randomize_starting_region == 0) and self.options.starting_scug != "Watcher"

        #################################################################
        # Universal Tracker support - use options from slot data if this is a fake generation
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data = re_gen_passthrough[self.game]

            # Set options based on slot data
            start_room = ""
            for key, value in slot_data.items():
                opt = getattr(self.options, key, None)
                if opt is not None:
                    setattr(self.options, key, opt.from_any(value))
                elif key == "starting_room":
                    start_room = value

            self.start_is_default = start_room == ""
            self.starting_room = get_default_start(self.options.starting_scug) \
                if start_room == "" else start_room.upper()

    def create_regions(self):
        # Create and resolve regions and entrances
        for data in regions.generate(self.options, self.random):
            data.make(self, self.options)

        # Create locations
        locs = [data for data in locations.generate(self.options)
                if data.pre_generate(self.player, self.multiworld, self.options)]
        # Need to remember which food quest locs were generated for accessibility flag
        foodquest_locs = [(data, data.pre_generate(self.player, self.multiworld, self.options))
                          for data in locations.generate_foodquest(self.options)]

        # Resolve locations
        genned_locs = locs + [l for l, v in foodquest_locs if v]
        for loc in genned_locs: loc.make(self, self.options)

        self.location_count = len(genned_locs)
        self.foodquest_accessibility_flag = sum(e << i for i, (_, e) in enumerate(foodquest_locs))

        # Create and resolve events
        for data in get_events(self.options, self.multiworld.get_regions(self.player)):
            data.make(self, self.options)

        #################################################################
        # STARTING REGION
        self.connect_starting_region(self.starting_room)

    def generate_basic(self) -> None:
        #################################################################
        # PRIORITY PASSAGES
        if (num := self.options.passage_priority.value) > 0:
            unprioritized_passage_locations = [
                l for l in self.multiworld.get_locations(self.player)
                if l.name.startswith("Passage - ") and l.progress_type == LocationProgressType.DEFAULT
            ]
            for loc in self.random.sample(unprioritized_passage_locations,
                                          min([num, len(unprioritized_passage_locations)])):
                loc.progress_type = LocationProgressType.PRIORITY

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
                "Longer Cycles": 1 if self.options.starting_scug == "Rivulet" else 0,
                "Disable Five Pebbles": 1 if self.options.starting_scug == "Rivulet" else 0,
                "Rarefaction Cell": 1 if self.options.starting_scug == "Rivulet" else 0,
                "Moon's Final Message": 1 if self.options.starting_scug == "Spear" else 0,
                "Spearmaster's Pearl": 1 if self.options.starting_scug == "Spear" else 0,
            }
        else:
            pool = {
                "Ripple": 12 + self.options.extra_karma_cap_increases.value,
                **{k: 1 for k, v in portal_keys.items() if (not v.spinning_top or self.options.spinning_top_keys)
                   and ("Daemon" not in v.name or self.options.daemon_keys)},
                "Progressive Weaver": 4 if self.options.weaver_randomized else 0,
                "Dial Warp Ability": 1,
                "The Mark": 1,
            }
            if self.options.watcher_passages:
                pool.update({f"Passage Token - {passage_proper_names[p]}": 1
                             for p in (passages_all if self.options.msc_enabled else passages_vanilla)})
            # if (ndwb := self.options.normal_dynamic_warp_behavior).unlockable:
            #     pool.update({f"Dynamic: {k}": 1 for k in (normal_regions if ndwb.predetermined else self.warp_pool)})

        if self.options.damage_upgrades > 0:
            pool.update({"Spear Damage Increase" : self.options.damage_upgrades})
        if self.options.msc_enabled:
            pool.update(**{perk : 1 for perk in self.options.expedition_perks})

        precollect = { }

        if self.options.starting_region_code == "MS":
            precollect.update({"Bubble Weed": 1})

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

    def get_filler_item_name(self) -> str:
        # Get a single random filler item, weighted by options
        weights = normalize(self.jitter(self.options.get_nontrap_weight_dict()))
        r = self.random.random()
        count = 0.0
        for k, v in weights.items():
            count += v
            if r <= count:
                return k

        return "Rock"

    def set_rules(self) -> None:
        # ascension_item = Item("Ascension", ItemClassification.progression, None, self.player)
        # self.multiworld.get_location("Ascension", self.player).place_locked_item(ascension_item)
        self.set_completion_rule(Simple("Victory").get_rule())
        # self.multiworld.completion_condition[self.player] = Simple("Victory").check(self.player)

    def fill_slot_data(self) -> Mapping[str, Any]:
        d = self.options.as_dict(
            # Plugin needs to know...
            "is_msc_enabled",  # ...whether MSC should be enabled.
            "is_watcher_enabled",  # ...whether The Watcher should be enabled.
            "which_campaign",  # ...which campaign should be selected.
            "passage_progress_without_survivor",  # ...if this setting doesn't match Remix.
            "death_link",  # ...whether to listen for death link notifications.
            "checks_foodquest",  # ...whether the food quest should be available.
            "checks_broadcasts",  # ...whether broadcasts should be available.
            "checks_tokens_pearls",  # ...whether all tokens should be available.
            "checks_sheltersanity",  # ...whether shelters are checks.
            "checks_flowersanity",  # ...whether karma flowers are checks.
            "checks_devtokens",  # ...whether dev tokens should be checks.
            "which_victory_condition",  # ...which victory condition is a win.
            "which_gate_behavior",  # ...how gates should behave.
            "difficulty_echo_low_karma",  # ...how low-karma echo appearances should be handled.
            "rotted_region_target",  # ...how many regions must be rotted for Watcher's alt ending.
            "spinning_top_keys",  # ...whether Spinning Top should appear without a key.
            "checks_spread_rot", # ...whether spreading rot should be checks.
            "checks_weaver_encounters", # ...whether encountering the Weaver should be checks.
            "randomize_weaver", # ...whether the Weaver ability is randomized.

            # External tracker needs to know...
            "difficulty_glow", "difficulty_monk", "difficulty_hunter", "difficulty_outlaw", "difficulty_chieftain",
            "difficulty_nomad", "difficulty_extreme_threats", "checks_submerged", "difficulty_submerged",
            "checks_foodquest_expanded", "logic_rotted_generation", "logic_ripplespace_min_req",
            "expedition_perks", "daemon_keys"
        )
        # backwards compatibility
        d["which_gamestate"] = self.options.which_gamestate_integer
        d["which_game_version"] = 1100400
        # ...which room to spawn in.  Empty string for default.
        d["starting_room"] = ("" if self.start_is_default
                              else ingame_capitalization.get(self.starting_room, self.starting_room))
        # ...which food quest checks are accessible.
        d["checks_foodquest_accessibility"] = (
            self.foodquest_accessibility_flag if self.options.checks_foodquest_expanded else 0)

        # temp override
        d["which_campaign"] = self.options.starting_scug

        # TODO: Change this when an official way to fetch world version from manifest exists
        import pkgutil
        from orjson import orjson
        apworld_manifest = orjson.loads(pkgutil.get_data(__name__, "archipelago.json").decode("utf-8"))
        d["apworld_version"] = apworld_manifest["world_version"]

        return d

    def generate_output(self, output_directory: str) -> None:
        if self.options.debug_output:
            import json
            from Utils import visualize_regions
            with open(f'{output_directory}/client_map.json', 'w') as f:
                json.dump({"locations": locations.classes.location_client_map, "items": items.item_client_names}, f)
            with open(f'{output_directory}/player_{self.player}_debug.json', 'w') as f:
                json.dump(fp=f, indent=2, obj={
                    "slot_data": self.fill_slot_data()
                })
            visualize_regions(self.multiworld.get_region("Menu", self.player), "rain_world.puml", show_locations=False)

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if not self.start_is_default:
            spoiler_handle.write(f"Starting Region: {self.options.starting_region_name}\n")

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        """Universal Tracker support - synchronize UT internal multiworld with actual slot data."""
        return slot_data
