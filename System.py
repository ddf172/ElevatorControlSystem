from Algorithm import *
from Singleton import Singleton


class System(Singleton):
    # Configuration
    # 0 - never
    new_person_in_moves = 4
    how_many_people_at_once = 1
    how_often_generate_new_path = 5
    runtime = 100

    def __init__(self, people=None, elevators=None, floor_number=10):
        if hasattr(self, 'initialized'): return
        self.initialized = True
        
        if people is None:
            people = []
        if elevators is None:
            elevators = []
        self.people = people
        self.elevators = elevators
        self.floor_number = floor_number
        self.transported_people = 0

    def add_person(self, start_pos=None, destination=None):
        if start_pos is None:
            start_pos = random.randint(0, self.floor_number-1)
        if destination is None:
            while destination is None or destination == start_pos:
                destination = random.randint(0, self.floor_number-1)

        person = Person(start_pos, destination)
        self.people.append(person)

    def add_elevator(self, position=0, capacity=5):
        elevator = Elevator(position, capacity)
        self.elevators.append(elevator)

    def remove_person(self, index):
        return self.people.pop(index)

    def make_path(self):
        algorithm = Algorithm(self.elevators, self.people, self.floor_number)
        best_member = algorithm.run_algorithm()
        for index, elevator in enumerate(best_member.elevators):
            self.elevators[index].path = elevator.path

    def make_move(self):
        for elevator in self.elevators:
            if not elevator.path:
                self.make_path()
                break
        for elevator in self.elevators:
            move = elevator.path[0]
            if move == 1:
                elevator.position += 1
            elif move == -1:
                elevator.position -= 1
            elif move == 2:
                people_to_remove = []
                for person_index, person in enumerate(elevator.people):
                    if person.destination == elevator.position:
                        people_to_remove.append(person_index)

                self.transported_people += len(people_to_remove)
                people_to_remove = sorted(people_to_remove, reverse=True)

                for person_index in people_to_remove:
                    elevator.people.pop(person_index)

                people_entering_elevator = []
                for person_index, person in enumerate(self.people):
                    if len(elevator.people) == elevator.capacity:
                        break
                    if person.start_pos == elevator.position:
                        people_entering_elevator.append(person_index)
                        elevator.people.append(person)

                people_entering_elevator = sorted(people_entering_elevator, reverse=True)
                for person_index in people_entering_elevator:
                    self.people.pop(person_index)

            elevator.path.pop(0)

    def run_system(self):
        when_to_add_person = 0
        when_to_generate_path = 0
        while self.runtime > 0:
            self.runtime -= 1
            self.make_move()

            # adding people in real time
            when_to_add_person += 1
            if when_to_add_person == self.new_person_in_moves:
                for i in range(self.how_many_people_at_once):
                    self.add_person()

                self.make_path()
                when_to_generate_path = 0
                when_to_add_person = 0

            # creating new path
            when_to_generate_path += 1
            if when_to_generate_path == self.how_often_generate_new_path:
                self.make_path()
                when_to_generate_path = 0




