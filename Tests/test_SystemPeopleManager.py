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
