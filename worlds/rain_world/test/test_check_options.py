from .bases import RainWorldTestBase

if RUN_GENERAL_AP_UNITTESTS := False:
    # Simply importing this runs the tests.
    from .bases import RainWorldGeneralTestBase

class TestChecksSubmergedAquatic(RainWorldTestBase):
    options = {"checks_submerged": "only_aquatic", "is_msc_enabled": True, "expedition_perks": ["Aquatic Perk"]}

    def test_check_generation(self):
        regions = [region.name for region in self.multiworld.get_regions(self.player)]
        self.assertIn("Submerged Superstructure", regions)
        self.assertIn("Shoreline near gate to Submerged", regions)

class TestChecksSubmergedAquaticFail(RainWorldTestBase):
    options = {"checks_submerged": "only_aquatic", "is_msc_enabled": True}

    def test_check_generation(self):
        regions = [region.name for region in self.multiworld.get_regions(self.player)]
        self.assertNotIn("Submerged Superstructure", regions)
        self.assertNotIn("Shoreline near gate to Submerged", regions)

class TestChecksSubmergedOff(RainWorldTestBase):
    options = {"checks_submerged": "off", "is_msc_enabled": True, "which_campaign": "Rivulet"}

    def test_check_generation(self):
        regions = [region.name for region in self.multiworld.get_regions(self.player)]
        self.assertNotIn("Submerged Superstructure", regions)
        self.assertNotIn("Shoreline near gate to Submerged", regions)