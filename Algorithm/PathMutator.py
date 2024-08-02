from random import choice, randint
from Settings import Settings
from Objects.Member import Member
from Objects.Elevator import AlgorithmElevator


class PathMutator:
    def __init__(self):
        self.settings = Settings.Settings()

    def get_move_mutation(self, move: int) -> int:
        possible_mutation = set(self.settings.path.path_possible_moves[move]) - {move}
        return choice(list(possible_mutation))

    def mutate_elevator_path(self, elevator: AlgorithmElevator) -> None:
        for i in range(self.settings.algorithm.path_length):
            if randint(0, 1000) < self.settings.algorithm.mutation_rate:
                elevator.state.path[i] = self.get_move_mutation(elevator.state.path[i])

    def mutate_member(self, member: Member) -> None:
        for elevator in member.elevators:
            self.mutate_elevator_path(elevator)

    def mutate_population(self, population: list[Member]) -> None:
        for member in population:
            self.mutate_member(member)
