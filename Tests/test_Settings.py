from src.Settings.Settings import Settings


def test_settings():
    settings1 = Settings()
    settings2 = Settings()
    assert settings1 is settings2
    assert settings1 is Settings.get_instance()
    assert settings2 is Settings.get_instance()
    assert settings1 is Settings()
    assert settings2 is Settings()