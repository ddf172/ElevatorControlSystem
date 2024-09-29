import pytest
from src.Settings.Settings import Settings
from src.Algorithm.Tabu import Tabu
from src.Managers.EvaluatorPeopleManager import EvaluatorPeopleManager
from src.Managers.SystemPeopleManager import SystemPeopleManager


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
def tabu():
    return Tabu([], 0, 0)


@pytest.fixture
def evaluator_people_manager():
    return EvaluatorPeopleManager()


@pytest.fixture
def system_people_manager():
    return SystemPeopleManager()

