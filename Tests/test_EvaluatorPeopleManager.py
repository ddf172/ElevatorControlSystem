import pytest
from Managers.EvaluatorPeopleManager import EvaluatorPeopleManager
from Objects.Person import AlgorithmPerson


@pytest.fixture
def evaluator_people_manager():
    return EvaluatorPeopleManager()


def test_init(evaluator_people_manager):
    assert evaluator_people_manager.moved_elevator_people == set()


def test_add_person(evaluator_people_manager):
    person = AlgorithmPerson(0, 1, None, None)
    evaluator_people_manager.add_person(person, None)
    assert person.id in evaluator_people_manager.containers[None].floors[person.start_pos]
    assert person.current_affiliation is None
    assert person.original_affiliation is None
    assert evaluator_people_manager.containers[None].count == 1

    person = AlgorithmPerson(0, 1, None, None)
    evaluator_people_manager.add_person(person, 0)
    assert person.id in evaluator_people_manager.containers[0].floors[person.destination]
    assert person.current_affiliation == 0
    assert person.original_affiliation is None
    assert evaluator_people_manager.containers[0].count == 1

    person = AlgorithmPerson(0, 2, 0, 0)
    evaluator_people_manager.add_person(person, 0)
    assert person.id in evaluator_people_manager.containers[0].floors[person.destination]
    assert person.current_affiliation == 0
    assert person.original_affiliation == 0
    assert evaluator_people_manager.containers[0].count == 2
