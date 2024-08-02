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

        self.move_handlers: Dict[int, Callable[[SystemElevator, AlgorithmElevator, int], None]] = {
            -1: self.handle_move_down,
            0: self.handle_no_move,
            1: self.handle_move_up,
            2: self.handle_door_open
        }

    def handle_move_down(self, sys_elevator: SystemElevator, alg_elevator: AlgorithmElevator, index: int) -> None:
        pass

    def handle_no_move(self, sys_elevator: SystemElevator, alg_elevator: AlgorithmElevator, index: int) -> None:
        pass

    def handle_move_up(self, sys_elevator: SystemElevator, alg_elevator: AlgorithmElevator, index: int) -> None:
        pass

    def handle_door_open(self, sys_elevator: SystemElevator, alg_elevator: AlgorithmElevator, index: int) -> None:
        pass

    def evaluate_elevator_move(self, sys_elevator: SystemElevator, alg_elevator: AlgorithmElevator, index: int) -> None:
        move = 2
        handler = self.move_handlers.get(move)
        handler(sys_elevator, alg_elevator, index)

    def evaluate_move(self, member: Member, index: int) -> None:
        for sys_elevator, alg_elevator in zip(member.elevators, self.elevators):
            self.evaluate_elevator_move(sys_elevator, alg_elevator, index)

    def evaluate(self, member: Member) -> None:
        for i in range(self.settings.path.path_length):
            self.evaluate_move(member, i)
