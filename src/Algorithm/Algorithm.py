import copy
from typing import List

from src.Objects.Member import Member
from src.Objects.Elevator import *
from src.Settings.Settings import Settings
from src.Patterns.Singleton import Singleton
from Tabu import Tabu
from Crossover import Crossover
from src.Algorithm.MemberEvaluator import MemberEvaluator
from src.Managers.Converter import convert
from src.Managers.SystemPeopleManager import SystemPeopleManager


class Algorithm(Singleton):

    def __init__(self, elevators: List[SystemElevator], people_manager: SystemPeopleManager):
        if hasattr(self, 'initialized'): return
        self.initialized = True

        self.elevators = elevators
        self.people_manager = people_manager
        self.population = []
        self.best_member = Member()
        self.settings = Settings()
        self.crossover = Crossover()

    def generate_member(self) -> Member:
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
        evaluator_people_manager = convert(self.people_manager)
        evaluator = MemberEvaluator(evaluator_people_manager, self.settings)
        for member in self.population:
            evaluator.evaluate(member)

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

    def run_algorithm(self) -> Member:
        # Initialize algorithm
        self.generate_population()
        iterations = self.settings.algorithm.iterations

        while iterations > 0:
            iterations -= 1
            self.crossover_population()
            self.mutate_population()
            # self.validate_and_repair_population()
            self.evaluate_population()
            self.select_population()
            self.save_best_member()
            # print(end - start, "one interation time, iterations left:", iterations, "best fitness: ", self.best_member.fitness)

        return self.best_member
