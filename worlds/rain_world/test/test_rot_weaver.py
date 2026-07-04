from .bases import RainWorldTestBase

if RUN_GENERAL_AP_UNITTESTS := False:
    # Simply importing this runs the tests.
    from .bases import RainWorldGeneralTestBase

# Test every combination of victory condition, rot spreading checks, and randomized weaver options to ensure they are behaving correctly
class RotWeaverTestBase(RainWorldTestBase):
    def assert_rot_checks(self):
        self.assertIn("Spread the Rot - Region #1", [loc.name for loc in self.multiworld.get_locations(self.player)])

    def assert_no_rot_checks(self):
        self.assertNotIn("Spread the Rot - Region #1", [loc.name for loc in self.multiworld.get_locations(self.player)])

    def assert_weaver_items(self):
        self.assertIn("Progressive Weaver", [item.name for item in self.multiworld.get_items()])

    def assert_no_weaver_items(self):
        self.assertNotIn("Progressive Weaver", [item.name for item in self.multiworld.get_items()])


class TestRotEndingRotChecksWeaverOn(RotWeaverTestBase):
    options = {
        "is_watcher_enabled": True,
        "which_campaign": "watcher",
        "which_victory_condition": "prince",
        "checks_spread_rot": "true",
        "randomize_weaver": "true"
    }

    def test_logic(self):
        self.assert_rot_checks()
        self.assert_no_weaver_items()


class TestRotEndingRotChecksWeaverOff(RotWeaverTestBase):
    options = {
        "is_watcher_enabled": True,
        "which_campaign": "watcher",
        "which_victory_condition": "prince",
        "checks_spread_rot": "true",
        "randomize_weaver": "false"
    }

    def test_logic(self):
        self.assert_rot_checks()
        self.assert_no_weaver_items()


class TestRotEndingNoRotChecksWeaverOn(RotWeaverTestBase):
    options = {
        "is_watcher_enabled": True,
        "which_campaign": "watcher",
        "which_victory_condition": "prince",
        "checks_spread_rot": "false",
        "randomize_weaver": "true"
    }

    def test_logic(self):
        self.assert_no_rot_checks()
        self.assert_no_weaver_items()


class TestRotEndingNoRotChecksWeaverOff(RotWeaverTestBase):
    options = {
        "is_watcher_enabled": True,
        "which_campaign": "watcher",
        "which_victory_condition": "prince",
        "checks_spread_rot": "false",
        "randomize_weaver": "false"
    }

    def test_logic(self):
        self.assert_no_rot_checks()
        self.assert_no_weaver_items()


class TestWeaverEndingRotChecksWeaverOn(RotWeaverTestBase):
    options = {
        "is_watcher_enabled": True,
        "which_campaign": "watcher",
        "which_victory_condition": "weaver",
        "checks_spread_rot": "true",
        "randomize_weaver": "true"
    }

    def test_logic(self):
        self.assert_no_rot_checks()
        self.assert_weaver_items()


class TestWeaverEndingRotChecksWeaverOff(RotWeaverTestBase):
    options = {
        "is_watcher_enabled": True,
        "which_campaign": "watcher",
        "which_victory_condition": "weaver",
        "checks_spread_rot": "true",
        "randomize_weaver": "false"
    }

    def test_logic(self):
        self.assert_no_rot_checks()
        self.assert_no_weaver_items()


class TestWeaverEndingNoRotChecksWeaverOn(RotWeaverTestBase):
    options = {
        "is_watcher_enabled": True,
        "which_campaign": "watcher",
        "which_victory_condition": "weaver",
        "checks_spread_rot": "false",
        "randomize_weaver": "true"
    }

    def test_logic(self):
        self.assert_no_rot_checks()
        self.assert_weaver_items()


class TestWeaverEndingNoRotChecksWeaverOff(RotWeaverTestBase):
    options = {
        "is_watcher_enabled": True,
        "which_campaign": "watcher",
        "which_victory_condition": "weaver",
        "checks_spread_rot": "false",
        "randomize_weaver": "false"
    }

    def test_logic(self):
        self.assert_no_rot_checks()
        self.assert_no_weaver_items()


class TestTopEndingRotChecksWeaverOn(RotWeaverTestBase):
    options = {
        "is_watcher_enabled": True,
        "which_campaign": "watcher",
        "which_victory_condition": "spinning_top",
        "checks_spread_rot": "true",
        "randomize_weaver": "true"
    }

    def test_logic(self):
        self.assert_no_rot_checks()
        self.assert_weaver_items()


class TestTopEndingRotChecksWeaverOff(RotWeaverTestBase):
    options = {
        "is_watcher_enabled": True,
        "which_campaign": "watcher",
        "which_victory_condition": "spinning_top",
        "checks_spread_rot": "true",
        "randomize_weaver": "false"
    }

    def test_logic(self):
        self.assert_rot_checks()
        self.assert_no_weaver_items()


class TestTopEndingNoRotChecksWeaverOn(RotWeaverTestBase):
    options = {
        "is_watcher_enabled": True,
        "which_campaign": "watcher",
        "which_victory_condition": "spinning_top",
        "checks_spread_rot": "false",
        "randomize_weaver": "true"
    }

    def test_logic(self):
        self.assert_no_rot_checks()
        self.assert_weaver_items()


class TestTopEndingNoRotChecksWeaverOff(RotWeaverTestBase):
    options = {
        "is_watcher_enabled": True,
        "which_campaign": "watcher",
        "which_victory_condition": "spinning_top",
        "checks_spread_rot": "false",
        "randomize_weaver": "false"
    }

    def test_logic(self):
        self.assert_no_rot_checks()
        self.assert_no_weaver_items()