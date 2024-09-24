from random import randint
from Settings.Settings import Settings
from typing import Union


class Person:
    person_id = 0

    def __init__(self, start_pos, destination, person_id=None):
        if person_id is not None:
            self.id = person_id
            Person.person_id = person_id + 1
        else:
            self.id = Person.person_id
            Person.person_id += 1
        self.start_pos = start_pos
        self.destination = destination
        self.settings = Settings()

    def set_start_pos(self, pos):
        if pos < self.settings.get_lowest_floor() or pos > self.settings.get_highest_floor():
            raise (ValueError("Position out of range"))
        self.start_pos = pos

    def set_destination(self, destination):
        if destination < self.settings.get_lowest_floor() or destination > self.settings.get_highest_floor():
            raise (ValueError("Destination out of range"))
        self.destination = destination

    def randomize(self):
        self.start_pos = self.set_start_pos(
            randint(self.settings.get_lowest_floor(), self.settings.get_highest_floor()))
        self.destination = self.set_destination(
            randint(self.settings.get_lowest_floor(), self.settings.get_highest_floor()))

    def get_id(self):
        return self.id

    def get_start_pos(self):
        return self.start_pos

    def get_destination(self):
        return self.destination


class AlgorithmPerson(Person):
    def __init__(self, start_pos: int, destination: int, current_affiliation: Union[None, int], original_affiliation: Union[None, int], person_id=None):
        super().__init__(start_pos, destination, person_id)
        self.current_affiliation = current_affiliation
        self.original_affiliation = original_affiliation
