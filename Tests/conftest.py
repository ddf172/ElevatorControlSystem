import pytest
from Settings.Settings import Settings
from Algorithm.Tabu import Tabu
from Managers.EvaluatorPeopleManager import EvaluatorPeopleManager
from Managers.SystemPeopleManager import SystemPeopleManager


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

