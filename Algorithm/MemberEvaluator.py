from Objects.Elevator import *
from Objects.Member import Member
from Objects.Person import *
from Settings.Settings import Settings
from typing import List, Dict


class MemberEvaluator:
    def __init__(self, elevators: List[SystemElevator], people: Dict[int, List[Person]]):
        self.people_original_elevator = {}
        self.elevators = elevators
        self.people = people
        self.settings = Settings()

    def evaluate_elevator_move(self, sys_elevator: SystemElevator, alg_elevator: AlgorithmElevator) -> None:
        pass

    def evaluate_move(self, member: Member) -> None:
        for sys_elevator, alg_elevator in zip(member.elevators, self.elevators):
            self.evaluate_elevator_move(sys_elevator, alg_elevator)

    def evaluate(self, member: Member) -> None:
        for _ in range(self.settings.path.path_length):
            self.evaluate_move(member)
