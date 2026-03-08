from .bases import RainWorldTestBase

if RUN_GENERAL_AP_UNITTESTS := False:
    # Simply importing this runs the tests.
    from .bases import RainWorldGeneralTestBase


class TestMonkVanilla(RainWorldTestBase):
    options = {"which_campaign": "monk"}


class TestSurvivorVanilla(RainWorldTestBase):
    options = {"which_campaign": "survivor"}


class TestHunterVanilla(RainWorldTestBase):
    options = {"which_campaign": "hunter"}


class TestMonkMSC(RainWorldTestBase):
    options = {"which_campaign": "monk", "is_msc_enabled": True}


class TestSurvivorMSC(RainWorldTestBase):
    options = {"which_campaign": "survivor", "is_msc_enabled": True}


class TestHunterMSC(RainWorldTestBase):
    options = {"which_campaign": "hunter", "is_msc_enabled": True}

    def test_check_generation(self):
        locs = [loc.name for loc in self.multiworld.get_locations(self.player)]
        self.assertNotIn("Garbage Wastes - Pearl - MS", locs)
        self.assertNotIn("Garbage Wastes - Arena Token - Scavenger", locs)
        self.assertNotIn("Sky Islands - Broadcast - Chatlog_SI0", locs)
        self.assertNotIn("Sky Islands - Broadcast - Chatlog_SI1", locs)
        self.assertIn("Sky Islands - Arena Token - KingVulture", locs)
        self.assertIn("Sky Islands - Pearl - SI_top", locs)


class TestHunterMSCShadedCitadel(RainWorldTestBase):
    options = {"which_campaign": "hunter", "random_starting_shelter": "shaded_citadel",
               "difficulty_echo_low_karma": 1, "is_msc_enabled": True}

    def test_karma_flower_absence(self):
        self.assertAccessDependency(["Shaded Citadel - Echo"], [["Karma", "Karma", "Karma", "Karma"]], True)


class TestGourmand(RainWorldTestBase):
    options = {"which_campaign": "gourmand", "is_msc_enabled": True}


class TestArtificer(RainWorldTestBase):
    options = {"which_campaign": "artificer", "is_msc_enabled": True}

    def test_check_generation(self):
        locs = [loc.name for loc in self.multiworld.get_locations(self.player)]
        self.assertNotIn("Garbage Wastes - Arena Token - BrotherLongLegs", locs)

    def test_connections(self):
        connections = [con.name for con in self.multiworld.get_entrances(self.player)]
        self.assertIn("Westward from SU_A22 to SU_A43", connections)
        self.assertIn("Westward from SU_C04 to SU_CAVE01", connections)


class TestRivulet(RainWorldTestBase):
    options = {"which_campaign": "rivulet", "is_msc_enabled": True}

    def test_86(self):
        # https://github.com/alphappy/ArchipelagoRW/issues/86
        locs = [loc.name for loc in self.multiworld.get_locations(self.player)]
        self.assertIn("Shaded Citadel - Arena Token - MirosBird", locs)


class TestSpear(RainWorldTestBase):
    options = {"which_campaign": "spearmaster", "is_msc_enabled": True}

    def test_check_generation(self):
        locs = [loc.name for loc in self.multiworld.get_locations(self.player)]
        self.assertIn("Garbage Wastes - Pearl - MS", locs)
        self.assertIn("Sky Islands - Broadcast - Chatlog_SI0", locs)
        self.assertIn("Sky Islands - Broadcast - Chatlog_SI1", locs)
        self.assertNotIn("Sky Islands - Arena Token - KingVulture", locs)
        self.assertNotIn("Sky Islands - Pearl - SI_top", locs)


class TestSaint(RainWorldTestBase):
    options = {"which_campaign": "saint", "is_msc_enabled": True}

    def test_connections(self):
        connections = [con.name for con in self.multiworld.get_entrances(self.player)]
        self.assertIn("Westward from SU_A22 to SU_A43", connections)
        self.assertIn("Westward from SU_C04 to SU_CAVE01", connections)


class TestSofanthiel(RainWorldTestBase):
    options = {"which_campaign": "sofanthiel", "is_msc_enabled": True}


class TestMonkMSCAlternate(RainWorldTestBase):
    options = {"which_campaign": "monk", "which_victory_condition": "story", "is_msc_enabled": True}


class TestSurvivorMSCAlternate(RainWorldTestBase):
    options = {"which_campaign": "survivor", "which_victory_condition": "story", "is_msc_enabled": True}


class TestHunterAlternate(RainWorldTestBase):
    options = {"which_campaign": "hunter", "which_victory_condition": "story"}


class TestGourmandAlternate(RainWorldTestBase):
    options = {"which_campaign": "gourmand", "which_victory_condition": "story", "is_msc_enabled": True}


class TestArtificerAlternate(RainWorldTestBase):
    options = {"which_campaign": "artificer", "which_victory_condition": "story", "is_msc_enabled": True}


class TestRivuletAlternate(RainWorldTestBase):
    options = {"which_campaign": "rivulet", "which_victory_condition": "story", "is_msc_enabled": True}


class TestSpearAlternate(RainWorldTestBase):
    options = {"which_campaign": "spearmaster", "which_victory_condition": "story", "is_msc_enabled": True}


class TestEchoes(RainWorldTestBase):
    options = {"which_victory_condition": "echoes"}


class TestSaintEchoes(RainWorldTestBase):
    options = {"which_campaign": "saint", "which_victory_condition": "echoes", "is_msc_enabled": True}


class TestFoodQuest(RainWorldTestBase):
    options = {"which_campaign": "survivor", "which_victory_condition": "food_quest", "is_msc_enabled": True}


class TestMSCFoodQuest(RainWorldTestBase):
    options = {"which_campaign": "survivor", "which_victory_condition": "food_quest", "is_msc_enabled": True}


class TestHunterFoodQuest(RainWorldTestBase):
    options = {"which_campaign": "hunter", "which_victory_condition": "food_quest", "is_msc_enabled": True}


class TestGourmandFoodQuest(RainWorldTestBase):
    options = {"which_campaign": "gourmand", "which_victory_condition": "food_quest", "is_msc_enabled": True}


class TestArtificerFoodQuest(RainWorldTestBase):
    options = {"which_campaign": "artificer", "which_victory_condition": "food_quest", "is_msc_enabled": True}


class TestRivuletFoodQuest(RainWorldTestBase):
    options = {"which_campaign": "rivulet", "which_victory_condition": "food_quest", "is_msc_enabled": True}


class TestSpearFoodQuest(RainWorldTestBase):
    options = {"which_campaign": "spearmaster", "which_victory_condition": "food_quest", "is_msc_enabled": True}


class TestSaintFoodQuest(RainWorldTestBase):
    options = {"which_campaign": "saint", "which_victory_condition": "food_quest", "is_msc_enabled": True}


class TestWatcher(RainWorldTestBase):
    options = {"which_campaign": "watcher", "is_watcher_enabled": True, "is_msc_enabled": True}

class TestWatcherRot(RainWorldTestBase):
    options = {"which_campaign": "watcher", "is_watcher_enabled": True, "is_msc_enabled": True,
               "which_victory_condition": "story"}

class TestWatcherWeaver(RainWorldTestBase):
    options = {"which_campaign": "watcher", "is_watcher_enabled": True, "is_msc_enabled": True,
               "which_victory_condition": "weaver"}

class TestWatcherTrueEnding(RainWorldTestBase):
    options = {"which_campaign": "watcher", "is_watcher_enabled": True, "is_msc_enabled": True,
               "which_victory_condition": "true_ending"}

