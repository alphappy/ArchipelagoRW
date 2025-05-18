from . import RainWorldTestBase


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


class TestSofanthiel(RainWorldTestBase):
    options = {"which_campaign": "sofanthiel", "is_msc_enabled": True}


class TestMonkMSCAlternate(RainWorldTestBase):
    options = {"which_campaign": "monk", "which_victory_condition": "alternate", "is_msc_enabled": True}


class TestSurvivorMSCAlternate(RainWorldTestBase):
    options = {"which_campaign": "survivor", "which_victory_condition": "alternate", "is_msc_enabled": True}


class TestGourmandAlternate(RainWorldTestBase):
    options = {"which_campaign": "gourmand", "which_victory_condition": "alternate", "is_msc_enabled": True}


class TestArtificerAlternate(RainWorldTestBase):
    options = {"which_campaign": "artificer", "which_victory_condition": "alternate", "is_msc_enabled": True}


class TestRivuletAlternate(RainWorldTestBase):
    options = {"which_campaign": "rivulet", "which_victory_condition": "alternate", "is_msc_enabled": True}


class TestSpearAlternate(RainWorldTestBase):
    options = {"which_campaign": "spearmaster", "which_victory_condition": "alternate", "is_msc_enabled": True}


class TestWatcher(RainWorldTestBase):
    options = {"which_campaign": "watcher", "is_watcher_enabled": True}
