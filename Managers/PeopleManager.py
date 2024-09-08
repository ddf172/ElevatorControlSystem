from abc import ABC, abstractmethod
from collections.abc import Container
from typing import Union, TypeVar, Generic
from Settings.Settings import Settings

T = TypeVar('T', bound='Person')


class PeopleContainer:
    def __init__(self):
        self.floors = {}
        for i in range(Settings().path.lowest_floor, Settings().path.highest_floor + 1):
            self.floors[i] = {}

        self.count = 0


class PeopleManager(ABC, Generic[T]):
    def __init__(self):
        self.settings = Settings()
        self.containers = dict()

        self.containers[None] = PeopleContainer()
        for i in range(self.settings.elevator.elevator_number):
            self.containers[i] = PeopleContainer()

    def add_person(self, person: T, where: Union[None, int], position: int = None) -> None:
        if position is None:
            position = person.start_pos if where is None else person.destination

        self.containers[where].floors[position][person.id] = person
        self.containers[where].count += 1

    @abstractmethod
    def remove_person(self, person: T, where: Union[None, int]) -> bool:
        pass

    @abstractmethod
    def move_person(self, person: T, from_where: Union[None, int], to_where: Union[None, int]) -> None:
        pass
