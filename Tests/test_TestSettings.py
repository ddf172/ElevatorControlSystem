from src.Settings.SettingsForTests import SettingsForTests


def test_test_settings():
    settings1 = SettingsForTests()
    settings2 = SettingsForTests()
    assert settings1 is not settings2
