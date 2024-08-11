from Objects.Elevator import *
from Objects.Member import Member
from Objects.Person import *
from Settings.Settings import Settings
from typing import List, Dict, Callable


class MemberEvaluator:
    def __init__(self, elevators: List[SystemElevator], people: Dict[int, List[Person]]):
        self.people_original_elevator = {}
        self.elevators = elevators
        self.people = people
        self.settings = Settings()

        self.move_handlers: Dict[int, Callable[[AlgorithmElevator, int], None]] = {
            -1: self.handle_move_down,
            0: self.handle_no_move,
            1: self.handle_move_up,
            2: self.handle_door_open
        }

    def apply_move_fitness(self, alg_elevator: AlgorithmElevator) -> None:
        alg_elevator.fitness += self.settings.fitness.move

    def handle_move_down(self, alg_elevator: AlgorithmElevator, index: int) -> None:
        pass

    def handle_no_move(self, alg_elevator: AlgorithmElevator, index: int) -> None:
        pass

    def handle_move_up(self, alg_elevator: AlgorithmElevator, index: int) -> None:
        pass

    def handle_door_open(self, alg_elevator: AlgorithmElevator, index: int) -> None:
        pass

    def evaluate_elevator_move(self, alg_elevator: AlgorithmElevator, index: int) -> None:
        move = alg_elevator.state.path[index]
        handler = self.move_handlers.get(move)
        handler(alg_elevator, index)

    def evaluate_move(self, member: Member, index: int) -> None:
        for sys_elevator, alg_elevator in zip(member.elevators, self.elevators):
            self.evaluate_elevator_move(alg_elevator, index)

    def evaluate(self, member: Member) -> None:
        for i in range(self.settings.path.path_length):
            self.evaluate_move(member, i)
