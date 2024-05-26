class Elevator:
    def __init__(self, position, capacity, last_move=0):
        self._people = []
        self._fitness = 0
        self._position = position
        self._capacity = capacity
        self._path = []
        self._last_move = last_move

    def add_person(self, person):
        pass

    def remove_person(self, person):
        pass

    def get_people(self):
        pass

    def set_last_move(self, move):
        pass

    def get_last_move(self):
        pass

    def set_fitness(self, value):
        pass

    def get_fitness(self):
        pass

    def set_path_step(self, index, value):
        pass

    def set_path(self, path):
        pass

    def get_path(self):
        pass


class Person:
    person_id = 0

    def __init__(self, start_pos, destination):
        self._id = Person.person_id
        Person.person_id += 1
        self._start_pos = start_pos
        self._destination = destination

    def set_start_pos(self, pos):
        pass

    def set_destination(self, destination):
        pass

    def randomize(self):
        pass

    def get_id(self):
        pass

    def get_start_pos(self):
        pass

    def get_destination(self):
        pass


class Member:
    def __init__(self):
        self._elevators = []
        self._fitness = 0

    def add_elevator(self, elevator):
        pass

    def get_elevator(self, index):
        pass

    def set_fitness(self, value):
        pass

    def get_fitness(self):
        pass
