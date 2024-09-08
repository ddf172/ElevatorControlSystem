from operator import index

import pytest

from Managers.PeopleManager import PeopleContainer
from Managers.SystemPeopleManager import SystemPeopleManager
from Objects.Person import Person
from Tests.conftest import settings


@pytest.fixture
def system_people_manager():
    return SystemPeopleManager()


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
