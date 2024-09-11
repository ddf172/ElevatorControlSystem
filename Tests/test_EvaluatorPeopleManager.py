import pytest
from Managers.EvaluatorPeopleManager import EvaluatorPeopleManager
from Objects.Person import AlgorithmPerson


@pytest.fixture
def evaluator_people_manager():
    return EvaluatorPeopleManager()


def test_init(evaluator_people_manager):
    assert evaluator_people_manager.moved_elevator_people == set()
