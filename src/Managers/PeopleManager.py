from abc import ABC
from typing import Union, TypeVar, Generic
from src.Settings.Settings import Settings

T = TypeVar('T', bound='Person')


class PeopleContainer:
    def __init__(self):
        self.floors = {}
        for i in range(Settings().path.lowest_floor, Settings().path.highest_floor + 1):
            self.floors[i] = {}

        self.count = 0

    @staticmethod
    def get_position(person, where):
        if where is None:
            return person.start_pos
        return person.destination

    def add_person(self, person, where=None):
        position = self.get_position(person, where)
        self.floors[position][person.id] = person
        self.count += 1

    def remove_person(self, person, where=None):
        position = self.get_position(person, where)
        if person.id in self.floors[position]:
            self.floors[position].pop(person.id)
            self.count -= 1
            return True
        return False


class PeopleManager(ABC, Generic[T]):
    def __init__(self):
        self.settings = Settings()
        self.containers = dict()

        self.containers[None] = PeopleContainer()
        for i in range(self.settings.elevator.elevator_number):
            self.containers[i] = PeopleContainer()

    def add_person(self, person: T, where: Union[None, int], position: int = None) -> None:
        self.containers[where].add_person(person, where)

    def remove_person(self, person: T, where: Union[None, int]) -> bool:
        return self.containers[where].remove_person(person, where)

    def move_person(self, person: T, from_where: Union[None, int], to_where: Union[None, int]) -> None:
        if not self.remove_person(person, from_where):
            raise IndexError("Person not found in the place")
        self.add_person(person, to_where)
