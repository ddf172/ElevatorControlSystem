import pytest
from Settings.Settings import Settings
from Algorithm.Tabu import Tabu


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
def tabu():
    return Tabu([], 0, 0)

