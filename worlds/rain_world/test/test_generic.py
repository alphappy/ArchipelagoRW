from . import RainWorldTestBase


class TestMonkVanilla(RainWorldTestBase):
    options = {"which_gamestate": "monk_vanilla"}


class TestSurvivorVanilla(RainWorldTestBase):
    options = {"which_gamestate": "survivor_vanilla"}


class TestHunterVanilla(RainWorldTestBase):
    options = {"which_gamestate": "hunter_vanilla"}


class TestMonkMSC(RainWorldTestBase):
    options = {"which_gamestate": "monk_msc"}


class TestSurvivorMSC(RainWorldTestBase):
    options = {"which_gamestate": "survivor_msc"}


class TestHunterMSC(RainWorldTestBase):
    options = {"which_gamestate": "hunter_msc"}

    def test_check_generation(self):
        locs = [loc.name for loc in self.multiworld.get_locations(self.player)]
        self.assertNotIn("Garbage Wastes - Pearl - MS", locs)
        self.assertNotIn("Garbage Wastes - Arena Token - Scavenger", locs)
        self.assertNotIn("Sky Islands - Broadcast - Chatlog_SI0", locs)
        self.assertNotIn("Sky Islands - Broadcast - Chatlog_SI1", locs)
        self.assertIn("Sky Islands - Arena Token - KingVulture", locs)
        self.assertIn("Sky Islands - Pearl - SI_top", locs)


class TestHunterMSCShadedCitadel(RainWorldTestBase):
    options = {"which_gamestate": "hunter_msc", "random_starting_shelter": "shaded_citadel",
               "difficulty_echo_low_karma": 1}

    def test_karma_flower_absence(self):
        self.assertAccessDependency(["Shaded Citadel - Echo"], [["Karma", "Karma", "Karma", "Karma"]], True)


class TestGourmand(RainWorldTestBase):
    options = {"which_gamestate": "gourmand"}


class TestArtificer(RainWorldTestBase):
    options = {"which_gamestate": "artificer"}

    def test_check_generation(self):
        locs = [loc.name for loc in self.multiworld.get_locations(self.player)]
        self.assertNotIn("Garbage Wastes - Arena Token - BrotherLongLegs", locs)


class TestRivulet(RainWorldTestBase):
    options = {"which_gamestate": "rivulet"}

    def test_86(self):
        # https://github.com/alphappy/ArchipelagoRW/issues/86
        locs = [loc.name for loc in self.multiworld.get_locations(self.player)]
        self.assertIn("Shaded Citadel - Arena Token - MirosBird", locs)


class TestSpear(RainWorldTestBase):
    options = {"which_gamestate": "spearmaster"}

    def test_check_generation(self):
        locs = [loc.name for loc in self.multiworld.get_locations(self.player)]
        self.assertIn("Garbage Wastes - Pearl - MS", locs)
        self.assertIn("Sky Islands - Broadcast - Chatlog_SI0", locs)
        self.assertIn("Sky Islands - Broadcast - Chatlog_SI1", locs)
        self.assertNotIn("Sky Islands - Arena Token - KingVulture", locs)
        self.assertNotIn("Sky Islands - Pearl - SI_top", locs)


class TestSaint(RainWorldTestBase):
    options = {"which_gamestate": "saint"}


class TestSofanthiel(RainWorldTestBase):
    options = {"which_gamestate": "sofanthiel"}


class TestMonkMSCAlternate(RainWorldTestBase):
    options = {"which_gamestate": "monk_msc", "which_victory_condition": "alternate"}


class TestSurvivorMSCAlternate(RainWorldTestBase):
    options = {"which_gamestate": "survivor_msc", "which_victory_condition": "alternate"}


class TestGourmandAlternate(RainWorldTestBase):
    options = {"which_gamestate": "gourmand", "which_victory_condition": "alternate"}


class TestArtificerAlternate(RainWorldTestBase):
    options = {"which_gamestate": "artificer", "which_victory_condition": "alternate"}


class TestRivuletAlternate(RainWorldTestBase):
    options = {"which_gamestate": "rivulet", "which_victory_condition": "alternate"}


class TestSpearAlternate(RainWorldTestBase):
    options = {"which_gamestate": "spearmaster", "which_victory_condition": "alternate"}
