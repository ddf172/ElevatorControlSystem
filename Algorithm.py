import random
import copy
import time
from Objects import *
from Singleton import Singleton
from Tabu import Tabu


class Algorithm(Singleton):

    def __init__(self, elevators, people, floor_number):
        if hasattr(self, 'initialized'): return
        self.initialized = True

        self.elevators = elevators
        self.people = people
        self.floor_number = floor_number
        self.population = []
        self.best_member = Member()
        self.settings = Settings()

    def generate_member(self):
        member = Member()
        for elevator in self.elevators:
            tabu = Tabu(elevator.state.path, elevator.state.curr_position, elevator.state.last_move_from_prev_iteration)
            tabu.generate_new_path()

            member_elevator = elevator.create_elevator_deepcopy()
            member_elevator.state.path = tabu.get_path()
            member.add_elevator(member_elevator)
        return member

    def generate_population(self):
        for _ in range(self.settings.population_size):
            member = self.generate_member()
            self.population.append(member)

    @staticmethod
    def validate_and_repair_member(member):
        for elevator in member.elevators:
            tabu = Tabu(elevator.state.path, elevator.state.curr_position, elevator.state.last_move_from_prev_iteration)
            tabu.validate_and_repair_path()
            elevator.state.path = tabu.get_path()

    def validate_and_repair_population(self):
        for member in self.population:
            self.validate_and_repair_member(member)

    def crossover_population(self):
        for i in range(0, self.settings.population_size, 2):
            new_member1 = Member()
            new_member2 = Member()
            for j in range(len(self.elevators)):
                parent1 = self.population[i].elevators[j]
                parent2 = self.population[i + 1].elevators[j]

                child1 = Elevator(parent1.curr_position, parent1.capacity, parent1.last_move)
                child1.people = copy.deepcopy(parent1.people)
                child2 = Elevator(parent2.curr_position, parent2.capacity, parent2.last_move)
                child2.people = copy.deepcopy(parent2.people)

                total_fitness = max(parent1.fitness, 0) + max(parent2.fitness, 0)
                if total_fitness == 0:
                    probabilities = [0.5, 0.5]
                else:
                    probabilities = [parent1.fitness / total_fitness, parent2.fitness / total_fitness]

                for k in range(self.path_length):
                    if parent1.path[k] == parent2.path[k]:
                        child1.path.append(parent1.path[k])
                        child2.path.append(parent1.path[k])
                    else:
                        child1.path.append(random.choices([parent1.path[k], parent2.path[k]], probabilities, k=1))
                        child2.path.append(random.choices([parent1.path[k], parent2.path[k]], probabilities, k=1))
                new_member1.elevators.append(child1)
                new_member2.elevators.append(child2)

            self.population.append(new_member1)
            self.population.append(new_member2)

    def select_population(self):
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        self.population = self.population[0:self.population_size]

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
                        for person in elevator.people:
                            if person.destination == elevator.curr_position:
                                missed_count += 1

                        elevator.fitness += missed_count * self.missed_destination_floor
                        elevator.fitness += self.journey_time * len(elevator.people)
                        elevator.fitness += self.move_penalty

                        elevator.curr_position += move

                    elif move == 0:
                        elevator.fitness += self.no_move
                        elevator.fitness += len(elevator.people) * self.no_move_with_passenger
                        elevator.fitness += len(elevator.people) * self.journey_time

                    else:
                        elevator.fitness += self.door_movement
                        people_to_remove = []
                        for person_index, person in enumerate(elevator.people):
                            if person.destination == elevator.curr_position:
                                people_to_remove.append(person_index)

                        people_to_remove = sorted(people_to_remove, reverse=True)

                        for person_index in people_to_remove:
                            elevator.people.pop(person_index)
                            elevator.fitness += self.drop_out

                        elevator.fitness += len(elevator.people) * self.journey_time

                        people_entering_elevator = []
                        for person_index, person in enumerate(people_copy):
                            if len(elevator.people) == elevator.capacity:
                                break
                            if person.start_pos == elevator.curr_position:
                                people_entering_elevator.append(person_index)
                                elevator.people.append(person)
                                elevator.fitness += self.pick_up

                        people_entering_elevator = sorted(people_entering_elevator, reverse=True)
                        for person_index in people_entering_elevator:
                            people_copy.pop(person_index)
                member.fitness += len(people_copy) * self.waiting_time

            for elevator in member.elevators:
                member.fitness += elevator.fitness
            member.elevators = elevators_copy

    def save_best_member(self):
        if self.best_member is None or self.best_member.fitness < self.population[0].fitness:
            self.best_member = copy.deepcopy(self.population[0])

    def mutate_population(self):
        for member in self.population:
            for elevator in member.elevators:
                for i in range(self.path_length):
                    if random.randint(0, 1000) < self.mutation_rate:
                        elevator.path[i] = random.randint(-1, 2)

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
