from Settings import Settings
from random import randint
from copy import deepcopy
from typing import List


class PathState:
    def __init__(self, path: List[int], position: int = 0, last_move: int = 0):
        self.path = path
        self.original_position = position
        self.curr_position = position
        self.last_move_from_prev_iteration = last_move


class Elevator:
    def __init__(self, position, capacity, last_move=0):
        self.people = []
        self.fitness = 0
        self.capacity = capacity
        self.state = PathState([], position, last_move)

    def create_elevator_deepcopy(self):
        elevator = Elevator(self.state.curr_position, self.capacity, self.state.last_move_from_prev_iteration)
        elevator.people = deepcopy(self.people)
        return elevator


class Person:
    person_id = 0

    def __init__(self, start_pos, destination):
        self._id = Person.person_id
        Person.person_id += 1
        self._start_pos = start_pos
        self._destination = destination
        self._settings = Settings()

    def set_start_pos(self, pos):
        if pos < self._settings.get_lowest_floor() or pos > self._settings.get_highest_floor():
            raise (ValueError("Position out of range"))
        self._start_pos = pos

    def set_destination(self, destination):
        if destination < self._settings.get_lowest_floor() or destination > self._settings.get_highest_floor():
            raise (ValueError("Destination out of range"))
        self._destination = destination

    def randomize(self):
        self._start_pos = self.set_start_pos(randint(self._settings.get_lowest_floor(), self._settings.get_highest_floor()))
        self._destination = self.set_destination(randint(self._settings.get_lowest_floor(), self._settings.get_highest_floor()))

    def get_id(self):
        return self._id

    def get_start_pos(self):
        return self._start_pos

    def get_destination(self):
        return self._destination


class Member:
    def __init__(self):
        self.elevators = []
        self._fitness = 0
        self._settings = Settings()

    def add_elevator(self, elevator):
        if len(self.elevators) == self._settings.get_elevator_number():
            raise (ValueError("Member already has 3 elevators"))

        if type(elevator) is not Elevator:
            raise (TypeError("Object is not of type Elevator"))
        if elevator in self.elevators:
            raise (ValueError("Elevator already in list"))
        self.elevators.append(elevator)

    def get_elevator(self, index):
        if index < 0 or index >= len(self.elevators):
            raise (IndexError("Index out of range"))
        return self.elevators[index]

    def set_fitness(self, value):
        self._fitness = value

    def get_fitness(self):
        return self._fitness
