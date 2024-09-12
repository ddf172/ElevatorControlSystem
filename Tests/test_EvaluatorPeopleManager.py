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


def test_remove_person(evaluator_people_manager):
    person = AlgorithmPerson(0, 1, None, None)
    evaluator_people_manager.add_person(person, None)
    assert evaluator_people_manager.remove_person(person, None)
    assert person.id not in evaluator_people_manager.containers[None].floors[person.start_pos]
    assert person.current_affiliation == -1
    assert evaluator_people_manager.containers[None].count == 0
    assert person in evaluator_people_manager.moved_elevator_people

    person = AlgorithmPerson(0, 1, None, None)
    evaluator_people_manager.add_person(person, 0)
    assert evaluator_people_manager.remove_person(person, 0)
    assert person.id not in evaluator_people_manager.containers[0].floors[person.destination]
    assert person.current_affiliation == -1
    assert evaluator_people_manager.containers[0].count == 0
    assert person in evaluator_people_manager.moved_elevator_people
    assert len(evaluator_people_manager.moved_elevator_people) == 2

    # Test remove person that is not in the container
    person = AlgorithmPerson(0, 1, None, None)
    evaluator_people_manager.add_person(person, None)
    assert not evaluator_people_manager.remove_person(person, 0)
    assert person.id in evaluator_people_manager.containers[None].floors[person.start_pos]
    assert person.current_affiliation is None
    assert evaluator_people_manager.containers[None].count == 1


def test_move_person(evaluator_people_manager):
    person = AlgorithmPerson(0, 1, None, None)
    evaluator_people_manager.add_person(person, None)
    evaluator_people_manager.move_person(person, None, 0)
    assert person.id in evaluator_people_manager.containers[0].floors[person.destination]
    assert person.current_affiliation == 0
    assert person.original_affiliation is None
    assert evaluator_people_manager.containers[0].count == 1
    assert person in evaluator_people_manager.moved_elevator_people

    person = AlgorithmPerson(0, 1, 0, 0)
    evaluator_people_manager.add_person(person, 0)
    evaluator_people_manager.move_person(person, 0, None)
    assert person.id in evaluator_people_manager.containers[None].floors[person.start_pos]
    assert person.current_affiliation is None
    assert person.original_affiliation == 0
    assert evaluator_people_manager.containers[None].count == 1
    assert person in evaluator_people_manager.moved_elevator_people


def test_rollback(evaluator_people_manager):
    person = AlgorithmPerson(0, 1, None, None)
    evaluator_people_manager.add_person(person, None)
    evaluator_people_manager.move_person(person, None, 0)
    assert person.id in evaluator_people_manager.containers[0].floors[person.destination]
    assert person.current_affiliation == 0

    evaluator_people_manager.rollback()
    assert person.id in evaluator_people_manager.containers[None].floors[person.start_pos]
    assert person.current_affiliation is None
    assert person.original_affiliation is None
    assert evaluator_people_manager.containers[None].count == 1
    assert evaluator_people_manager.containers[0].count == 0
    assert len(evaluator_people_manager.moved_elevator_people) == 0

    person = AlgorithmPerson(0, 1, 0, 0)
    evaluator_people_manager.add_person(person, 0)
    evaluator_people_manager.move_person(person, 0, None)
    evaluator_people_manager.rollback()
    assert person.id in evaluator_people_manager.containers[0].floors[person.destination]
    assert person.current_affiliation == 0
    assert person.original_affiliation == 0
    assert evaluator_people_manager.containers[0].count == 1
    assert len(evaluator_people_manager.moved_elevator_people) == 0
