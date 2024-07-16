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
        self._state = PathState([], position, last_move)
        self._people = []
        self._fitness = 0
        self._capacity = capacity
        self._settings = Settings()

    def add_person(self, person):
        self._people.append(person)

    def remove_person(self, person):
        return self._people.remove(person)

    def set_people(self, people):
        if len(people) > self._capacity:
            raise (ValueError("People list exceeds capacity"))
        self._people = people

    def get_people(self):
        return self._people

    def set_last_move(self, move):
        if not self._state.path:
            self._state.path.append(move)
        else:
            self._state.path[-1] = move

    def get_last_move(self):
        if not self._state.path:
            return None
        return self._state.path[-1]

    def set_fitness(self, value):
        self._fitness = value

    def get_fitness(self):
        return self._fitness

    def set_path_step(self, index, value):
        if index < len(self._state.path):
            raise (IndexError("Index out of range"))
        if value not in [-1, 0, 1, 2]:
            raise (ValueError("Value not in [-1, 0, 1, 2]"))
        self._state.path[index] = value

    def set_path(self, path):
        if len(path) != self._settings.get_path_length():
            raise (ValueError("Path length does not match"))
        for index, value in enumerate(path):
            self.set_path_step(index, value)

    def get_path(self):
        return self._state.path

    def create_elevator_deepcopy(self):
        elevator = Elevator(self._state.curr_position, self._capacity, self.get_last_move())
        elevator.set_people(deepcopy(self._people))
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
        self._elevators = []
        self._fitness = 0
        self._settings = Settings()

    def add_elevator(self, elevator):
        if len(self._elevators) == self._settings.get_elevator_number():
            raise (ValueError("Member already has 3 elevators"))

        if elevator is not Elevator:
            raise (TypeError("Object is not of type Elevator"))
        if elevator in self._elevators:
            raise (ValueError("Elevator already in list"))
        self._elevators.append(elevator)

    def get_elevator(self, index):
        if index < 0 or index >= len(self._elevators):
            raise (IndexError("Index out of range"))
        return self._elevators[index]

    def set_fitness(self, value):
        self._fitness = value

    def get_fitness(self):
        return self._fitness
