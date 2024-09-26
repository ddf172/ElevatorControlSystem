import Managers.Converter as Converter
from Objects.Person import AlgorithmPerson, Person


def assert_person_conversion(person, algorithm_person, where):
    assert algorithm_person.start_pos == person.start_pos
    assert algorithm_person.destination == person.destination
    assert algorithm_person.current_affiliation == where
    assert algorithm_person.original_affiliation == where
    assert algorithm_person.id == person.id


def test_convert_person():
    person = Person(0, 1)
    algorithm_person = Converter._convert_person(person, None)
    assert isinstance(algorithm_person, AlgorithmPerson)
    assert_person_conversion(person, algorithm_person, None)

    person = Person(0, 1)
    algorithm_person = Converter._convert_person(person, 0)
    assert isinstance(algorithm_person, AlgorithmPerson)
    assert_person_conversion(person, algorithm_person, 0)


def test_convert_floor(evaluator_people_manager):
    people = {0: Person(0, 1), 1: Person(0, 1)}
    Converter._convert_floor(people, None, 0, evaluator_people_manager)
    assert len(evaluator_people_manager.containers[None].floors[0]) == 2

    assert_person_conversion(people[0], evaluator_people_manager.containers[None].floors[0][people[0].id], None)
    assert_person_conversion(people[1], evaluator_people_manager.containers[None].floors[0][people[1].id], None)

    for floor in evaluator_people_manager.containers[None].floors:
        if floor != 0:
            assert len(evaluator_people_manager.containers[None].floors[floor]) == 0

    people = {0: Person(0, 1, 10), 1: Person(0, 1, 11)}
    Converter._convert_floor(people, 0, 0, evaluator_people_manager)
    assert len(evaluator_people_manager.containers[0].floors[1]) == 2

    assert_person_conversion(people[0], evaluator_people_manager.containers[0].floors[1][people[0].id], 0)
    assert_person_conversion(people[1], evaluator_people_manager.containers[0].floors[1][people[1].id], 0)

    for floor in evaluator_people_manager.containers[0].floors:
        if floor != 1:
            assert len(evaluator_people_manager.containers[0].floors[floor]) == 0
