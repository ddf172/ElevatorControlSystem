from src.Managers.SystemPeopleManager import SystemPeopleManager
from src.Objects.Elevator import SystemElevator
from src.Settings.Settings import Settings
import random
from src.Objects.Person import Person
from src.Algorithm.Algorithm import Algorithm
from typing import List


class System:
    def __init__(self, elevators: List[SystemElevator] = None, people: List[Person] = None):

        self.algorithm = None
        self.people_manager = SystemPeopleManager()
        self.settings = Settings()
        self.transported_people = 0
        self.elevators = elevators

        if elevators is None:
            for i in range(self.settings.elevator.elevator_number):
                self.elevators.append(SystemElevator(0))

        if people is not None:
            for person in people:
                self.people_manager.add_person(person, None)

    def add_person(self, start_pos=None, destination=None) -> None:
        if start_pos is None:
            start_pos = random.randint(self.settings.get_lowest_floor(), self.settings.get_highest_floor())
        if destination is None:
            while destination is None or destination == start_pos:
                destination = random.randint(self.settings.get_lowest_floor(), self.settings.get_highest_floor())

        person = Person(start_pos, destination)
        self.people_manager.add_person(person, None)

    def remove_person(self, person, where) -> bool:
        return self.people_manager.remove_person(person, where)

    def make_path(self) -> None:
        self.algorithm = Algorithm(self.elevators, self.people_manager)
        best_member = self.algorithm.run_algorithm()
        for elevator_index, elevator in enumerate(self.elevators):
            elevator.state.path = best_member.get_elevator(elevator_index).state.path

    def make_move(self):
        for elevator_index, elevator in enumerate(self.elevators):
            assert len(elevator.state.path) > 0

            move = elevator.state.path.pop(0)
            if move == 1:
                elevator.state.position += 1
            elif move == -1:
                elevator.state.position -= 1
            elif move == 2:
                # Handle drop out
                people_to_drop = self.people_manager.containers[elevator_index].floors[elevator.state.position]
                people_to_drop_ids = list(people_to_drop.keys())
                for person_id in people_to_drop_ids:
                    self.people_manager.remove_person(people_to_drop[person_id], elevator_index)

                self.transported_people += len(people_to_drop_ids)

                # Handle pick up
                people_to_pick = self.people_manager.containers[None].floors[elevator.state.position]
                people_to_pick_ids = list(people_to_pick.keys())
                for person_id in people_to_pick_ids:
                    if self.people_manager.containers[elevator_index].count >= self.settings.elevator.elevator_capacity:
                        break
                    self.people_manager.move_person(people_to_pick[person_id], None, elevator_index)

    def run_system(self):
        when_to_add_person = 0
        when_to_generate_path = 0

        self.make_path()
        while self.settings.system.runtime > 0:
            self.settings.system.runtime -= 1

            # adding people in real time
            when_to_add_person += 1
            if when_to_add_person == self.settings.system.new_person_interval:
                for i in range(self.settings.system.people_batch_size):
                    self.add_person()

                self.make_path()
                when_to_generate_path = 0
                when_to_add_person = 0

            # creating new path
            when_to_generate_path += 1
            if when_to_generate_path == self.settings.system.path_generation_interval:
                self.make_path()
                when_to_generate_path = 0

            self.make_move()
