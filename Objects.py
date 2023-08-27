class Elevator:
    def __init__(self, position, capacity, last_move=0):
        self.people = []
        self.fitness = 0
        self.position = position
        self.capacity = capacity
        self.path = []
        self.last_move = last_move


class Person:
    person_id = 0

    def __init__(self, start_pos, destination):
        self.id = self.person_id
        self.person_id += 1
        self.start_pos = start_pos
        self.destination = destination


class Member:
    def __init__(self):
        self.elevators = []
        self.fitness = 0
