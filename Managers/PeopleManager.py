from abc import ABC
from typing import Union, TypeVar, Generic
from Settings.Settings import Settings

T = TypeVar('T', bound='Person')


class PeopleManager(ABC, Generic[T]):
    def __init__(self):
        self.settings = Settings()
        self.waiting_people = {}
        self.elevator_people = [{} for _ in range(self.settings.elevator.elevator_number)]
        self._setup_manager()

    def _setup_manager(self):
        for i in range(self.settings.get_lowest_floor(), self.settings.get_highest_floor() + 1):
            self.waiting_people[i] = {}

            for j in range(self.settings.elevator.elevator_number):
                self.elevator_people[j][i] = {}

    def _add_waiting_person(self, person: T) -> None:
        self.waiting_people[person.start_pos][person.id] = person

    def _add_elevator_person(self, person: T, elevator_index: int) -> None:
        self.elevator_people[elevator_index][person.destination][person.id] = person

    def _remove_waiting_person(self, person: T) -> bool:
        if person.id in self.waiting_people[person.start_pos]:
            self.waiting_people[person.start_pos].pop(person.id)
            return True
        return False

    def _remove_elevator_person(self, person: T, elevator_index: int) -> bool:
        if person.id in self.elevator_people[elevator_index][person.destination]:
            self.elevator_people[elevator_index][person.destination].pop(person.id)
            return True
        return False

    def add_person(self, person: T, where: Union[None, int]) -> None:
        if where is None:
            self._add_waiting_person(person)
        else:
            self._add_elevator_person(person, where)

    def remove_person(self, person: T, where: Union[None, int]) -> bool:
        if where is None:
            return self._remove_waiting_person(person)
        else:
            return self._remove_elevator_person(person, where)

    def move_person(self, person: T, from_where: Union[None, int], to_where: Union[None, int]) -> None:
        if not self.remove_person(person, from_where):
            raise ValueError("Person not found in the place")
        self.add_person(person, to_where)
