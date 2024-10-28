import pytest
from src.Managers.PeopleManager import PeopleContainer
from src.Objects.Person import Person


def test_init(system_people_manager, settings):
    assert len(system_people_manager.containers) == settings.elevator.elevator_number + 1
    assert None in system_people_manager.containers
    assert isinstance(system_people_manager.containers[None], PeopleContainer)

    for i in range(settings.elevator.elevator_number):
        assert i in system_people_manager.containers
        assert isinstance(system_people_manager.containers[i], PeopleContainer)


def test_add_person(system_people_manager, settings):
    # in None start_pos is floor index, in others destination is floor index
    person = Person(0, 1)
    system_people_manager.add_person(person, None)

    assert person.id in system_people_manager.containers[None].floors[person.start_pos]
    assert system_people_manager.containers[None].count == 1

    person = Person(0, 1)
    system_people_manager.add_person(person, None)

    assert person.id in system_people_manager.containers[None].floors[person.start_pos]
    assert system_people_manager.containers[None].count == 2

    person = Person(0, 1)
    system_people_manager.add_person(person, 0)

    assert person.id in system_people_manager.containers[0].floors[person.destination]
    assert system_people_manager.containers[0].count == 1

    with pytest.raises(KeyError):
        person = Person(0, 1)
        system_people_manager.add_person(person, settings.elevator.elevator_number)


def test_remove_person(system_people_manager, settings):
    person = Person(0, 1)
    system_people_manager.add_person(person, None)

    assert person.id in system_people_manager.containers[None].floors[person.start_pos]
    assert system_people_manager.containers[None].count == 1

    assert system_people_manager.remove_person(person, None)
    assert person.id not in system_people_manager.containers[None].floors[person.start_pos]
    assert system_people_manager.containers[None].count == 0

    assert not system_people_manager.remove_person(person, None)

    person = Person(0, 1)
    system_people_manager.add_person(person, 0)

    assert person.id in system_people_manager.containers[0].floors[person.destination]
    assert system_people_manager.containers[0].count == 1

    assert system_people_manager.remove_person(person, 0)
    assert person.id not in system_people_manager.containers[0].floors[person.destination]
    assert system_people_manager.containers[0].count == 0

    assert not system_people_manager.remove_person(person, 0)


def test_move_person(system_people_manager, settings):
    person = Person(0, 1)
    system_people_manager.add_person(person, None)

    assert person.id in system_people_manager.containers[None].floors[person.start_pos]
    assert system_people_manager.containers[None].count == 1

    system_people_manager.move_person(person, None, 0)

    assert person.id in system_people_manager.containers[0].floors[person.destination]
    assert system_people_manager.containers[0].count == 1
    assert person.id not in system_people_manager.containers[None].floors[person.start_pos]
    assert system_people_manager.containers[None].count == 0

    with pytest.raises(IndexError):
        system_people_manager.move_person(person, None, 0)
