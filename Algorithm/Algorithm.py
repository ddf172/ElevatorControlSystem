import copy
import time
from typing import List, Dict
from Objects.Member import Member
from Objects.Elevator import *
from Settings.Settings import Settings
from Singleton import Singleton
from Tabu import Tabu
from Crossover import Crossover


class Algorithm(Singleton):

    def __init__(self, elevators: List[SystemElevator], people: Dict[int, List[Person]]):
        if hasattr(self, 'initialized'): return
        self.initialized = True

        self.elevators = elevators
        self.people = people

        self.population = []
        self.best_member = Member()
        self.settings = Settings()
        self.crossover = Crossover()

    def generate_member(self) -> Member:
        # Divide into more functions
        member = Member()
        for elevator in self.elevators:
            tabu = Tabu([], elevator.state.position, elevator.state.last_move_from_prev_iteration)
            tabu.generate_new_path()

            member_elevator = AlgorithmElevator(elevator.state.position, elevator.state.last_move_from_prev_iteration)
            member_elevator.state.path = tabu.get_path()
            member.add_elevator(member_elevator)
        return member

    def generate_population(self) -> None:
        for _ in range(self.settings.algorithm.population_size):
            member = self.generate_member()
            self.population.append(member)

    @staticmethod
    def validate_and_repair_member(member: Member) -> None:
        for elevator in member.elevators:
            tabu = Tabu(elevator.state.path, elevator.state.position, elevator.state.last_move_from_prev_iteration)
            tabu.validate_and_repair_path()
            elevator.state.path = tabu.get_path()

    def validate_and_repair_population(self) -> None:
        for member in self.population:
            self.validate_and_repair_member(member)

    def crossover_population(self) -> None:
        self.crossover.crossover_population(self.population)

    def select_population(self) -> None:
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        self.population = self.population[0:self.settings.algorithm.population_size]

    def evaluate_population(self):
        for member in self.population:
            people_copy = copy.deepcopy(self.people)
            member.fitness = 0
            elevators_copy = copy.deepcopy(member.elevators)
            for index in range(self.path_length):
                for elevator in member.elevators:
                    move = elevator.path[index]

                    if move == 1 or move == -1:
                        missed_count = 0
                        for person in elevator.floors:
                            if person.destination == elevator.curr_position:
                                missed_count += 1

                        elevator.fitness += missed_count * self.missed_destination_floor
                        elevator.fitness += self.journey_time * len(elevator.floors)
                        elevator.fitness += self.move_penalty

                        elevator.curr_position += move

                    elif move == 0:
                        elevator.fitness += self.no_move
                        elevator.fitness += len(elevator.floors) * self.no_move_with_passenger
                        elevator.fitness += len(elevator.floors) * self.journey_time

                    else:
                        elevator.fitness += self.door_movement
                        people_to_remove = []
                        for person_index, person in enumerate(elevator.floors):
                            if person.destination == elevator.curr_position:
                                people_to_remove.append(person_index)

                        people_to_remove = sorted(people_to_remove, reverse=True)

                        for person_index in people_to_remove:
                            elevator.floors.pop(person_index)
                            elevator.fitness += self.drop_out

                        elevator.fitness += len(elevator.floors) * self.journey_time

                        people_entering_elevator = []
                        for person_index, person in enumerate(people_copy):
                            if len(elevator.floors) == elevator.capacity:
                                break
                            if person.start_pos == elevator.curr_position:
                                people_entering_elevator.append(person_index)
                                elevator.floors.append(person)
                                elevator.fitness += self.pick_up

                        people_entering_elevator = sorted(people_entering_elevator, reverse=True)
                        for person_index in people_entering_elevator:
                            people_copy.pop(person_index)
                member.fitness += len(people_copy) * self.waiting_time

            for elevator in member.elevators:
                member.fitness += elevator.fitness
            member.elevators = elevators_copy

    def save_best_member(self) -> None:
        # Assuming that the population is sorted by fitness in descending order

        current_generation_best = self.population[0]
        if self.best_member is None or self.best_member.fitness < current_generation_best.fitness:
            self.best_member = copy.deepcopy(current_generation_best)

    def mutate_population(self) -> None:
        for member in self.population:
            for elevator in member.elevators:
                tabu = Tabu(elevator.state.path, elevator.state.position, elevator.state.last_move_from_prev_iteration)
                tabu.mutate_elevator_path()
                elevator.state.path = tabu.get_path()

    def run_algorithm(self):
        self.generate_population()
        iterations = self.generations
        while iterations > 0:
            iterations -= 1
            start = time.time()
            self.crossover_population()
            self.mutate_population()
            self.validate_population()
            self.evaluate_population()
            self.select_population()
            self.save_best_member()
            end = time.time()
            # print(end - start, "one interation time, iterations left:", iterations, "best fitness: ", self.best_member.fitness)

        return self.best_member
