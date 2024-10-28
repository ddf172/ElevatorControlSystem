import src.Managers.Converter as Converter
from src.Objects.Person import AlgorithmPerson, Person
from src.Managers.PeopleManager import PeopleContainer


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


def test_convert_container(evaluator_people_manager):
    container = PeopleContainer()
    container.add_person(Person(0, 1), None)
    container.add_person(Person(0, 1), None)
    container.add_person(Person(0, 1, 10), None)
    container.add_person(Person(0, 1, 11), None)

    Converter._convert_container(container, None, evaluator_people_manager)
    assert len(evaluator_people_manager.containers[None].floors[0]) == 4

    for floor in evaluator_people_manager.containers[None].floors:
        if floor != 0:
            assert len(evaluator_people_manager.containers[None].floors[floor]) == 0

    for floor in evaluator_people_manager.containers[0].floors:
        assert len(evaluator_people_manager.containers[0].floors[floor]) == 0

    container = PeopleContainer()
    container.add_person(Person(0, 1, 20), 0)
    container.add_person(Person(0, 1, 21), 0)
    container.add_person(Person(0, 1, 22), 0)
    container.add_person(Person(0, 1, 23), 0)

    Converter._convert_container(container, 0, evaluator_people_manager)
    assert len(evaluator_people_manager.containers[0].floors[1]) == 4

    for floor in evaluator_people_manager.containers[0].floors:
        if floor != 1:
            assert len(evaluator_people_manager.containers[0].floors[floor]) == 0


def test_convert(evaluator_people_manager, system_people_manager, settings):
    system_people_manager.containers[None].add_person(Person(0, 1, 0), None)
    system_people_manager.containers[None].add_person(Person(0, 1, 1), None)
    system_people_manager.containers[None].add_person(Person(0, 1, 10), None)
    system_people_manager.containers[None].add_person(Person(0, 1, 11), None)

    system_people_manager.containers[0].add_person(Person(0, 1, 20), 0)
    system_people_manager.containers[0].add_person(Person(0, 1, 21), 0)
    system_people_manager.containers[0].add_person(Person(0, 1, 22), 0)
    system_people_manager.containers[0].add_person(Person(0, 1, 23), 0)

    evaluator_people_manager = Converter.convert(system_people_manager)
    assert len(evaluator_people_manager.containers) == settings.elevator.elevator_number + 1
    assert len(evaluator_people_manager.containers[None].floors) == settings.path.highest_floor - settings.path.lowest_floor + 1
    assert len(evaluator_people_manager.containers[0].floors) == settings.path.highest_floor - settings.path.lowest_floor + 1

    for floor in evaluator_people_manager.containers[None].floors:
        if floor != 0:
            assert len(evaluator_people_manager.containers[None].floors[floor]) == 0

    for floor in evaluator_people_manager.containers[0].floors:
        if floor != 1:
            assert len(evaluator_people_manager.containers[0].floors[floor]) == 0

    assert_person_conversion(system_people_manager.containers[None].floors[0][0], evaluator_people_manager.containers[None].floors[0][0], None)
    assert_person_conversion(system_people_manager.containers[None].floors[0][1], evaluator_people_manager.containers[None].floors[0][1], None)
    assert_person_conversion(system_people_manager.containers[None].floors[0][10], evaluator_people_manager.containers[None].floors[0][10], None)
    assert_person_conversion(system_people_manager.containers[None].floors[0][11], evaluator_people_manager.containers[None].floors[0][11], None)

    assert_person_conversion(system_people_manager.containers[0].floors[1][20], evaluator_people_manager.containers[0].floors[1][20], 0)
    assert_person_conversion(system_people_manager.containers[0].floors[1][21], evaluator_people_manager.containers[0].floors[1][21], 0)
    assert_person_conversion(system_people_manager.containers[0].floors[1][22], evaluator_people_manager.containers[0].floors[1][22], 0)
    assert_person_conversion(system_people_manager.containers[0].floors[1][23], evaluator_people_manager.containers[0].floors[1][23], 0)

    Person.person_id = 0
    AlgorithmPerson.person_id = 0
