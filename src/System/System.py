from src.Managers.SystemPeopleManager import SystemPeopleManager
from src.Objects.Elevator import SystemElevator
from src.Settings.Settings import Settings
import random
from src.Objects.Person import Person
from src.Algorithm.Algorithm import Algorithm
from typing import List
from collections import deque


class System:
    def __init__(self, elevators: List[SystemElevator] = None, people: List[Person] = None):

        self.people_manager = SystemPeopleManager()
        self.settings = Settings()
        self.transported_people = deque()
        self.elevators = elevators
        self.people_adding_interval = 0
        self.path_generation_interval = 0

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
        if self.people_manager.remove_person(person, where):
            self.transported_people.append(person)
            if len(self.transported_people) > self.settings.system.transported_people_track_number:
                self.transported_people.popleft()
            return True
        return False

    def make_path(self) -> None:
        algorithm = Algorithm(self.elevators, self.people_manager)
        best_member = algorithm.run_algorithm()
        print(best_member.fitness)
        for elevator_index, elevator in enumerate(self.elevators):
            elevator.state.path = best_member.get_elevator(elevator_index).state.path

    def apply_path_move(self):
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

    def handle_people_adding_interval(self):
        self.people_adding_interval += 1
        if self.people_adding_interval == self.settings.system.new_person_interval:
            for i in range(self.settings.system.people_batch_size):
                self.add_person()
            self.people_adding_interval = 0
            # path handling
            self.make_path()
            self.path_generation_interval = 0

    def handle_path_generation_interval(self):
        if not self.elevators[0].state.path:
            self.make_path()
            return

        self.path_generation_interval += 1
        if self.path_generation_interval == self.settings.system.path_generation_interval:
            self.make_path()
            self.path_generation_interval = 0

    def make_move(self) -> None:
        self.handle_people_adding_interval()
        self.handle_path_generation_interval()
        self.apply_path_move()

    def run_system(self):
        self.make_path()
        while self.settings.system.runtime > 0:
            self.settings.system.runtime -= 1
            self.make_move()
