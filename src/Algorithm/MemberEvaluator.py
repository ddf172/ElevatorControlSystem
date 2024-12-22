from src.Objects.Elevator import *
from src.Objects.Member import Member
from src.Settings.AbstractSettings import AbstractSettings
from src.Settings.Settings import Settings
from src.Managers.EvaluatorPeopleManager import EvaluatorPeopleManager
from typing import Dict, Callable, Optional, TypeVar


T = TypeVar('T', bound=AbstractSettings)


class MemberEvaluator:
    def __init__(self, people_manager: EvaluatorPeopleManager, settings: Optional[T] = None) -> None:
        self.people_manager = people_manager
        if settings is None:
            self.settings = Settings()
        else:
            self.settings = settings

        self.move_handlers: Dict[int, Callable[[AlgorithmElevator, int], None]] = {
            -1: self.handle_move_down,
            0: self.handle_no_move,
            1: self.handle_move_up,
            2: self.handle_door_open
        }

    def handle_fitness(self, arg_elevator: AlgorithmElevator, key: str, multiplier: int = 1) -> None:
        fitness_dict = self.settings.fitness.to_dict()
        arg_elevator.fitness += fitness_dict[key] * multiplier

    def handle_move(self, arg_elevator: AlgorithmElevator, elevator_index: int) -> None:
        self.handle_fitness(arg_elevator, 'move')

        # Handle missed destination floor
        for _ in self.people_manager.containers[elevator_index].floors[arg_elevator.state.position]:
            self.handle_fitness(arg_elevator, "missed_destination_floor")

    def handle_move_down(self, alg_elevator: AlgorithmElevator, elevator_index: int) -> None:
        self.handle_move(alg_elevator, elevator_index)

        alg_elevator.state.position -= 1

    def handle_no_move(self, alg_elevator: AlgorithmElevator, elevator_index: int) -> None:
        self.handle_fitness(alg_elevator, 'no_move')
        # Handle no move with passenger
        self.handle_fitness(alg_elevator, 'no_move_with_passenger', self.people_manager.containers[elevator_index].count)

    def handle_move_up(self, alg_elevator: AlgorithmElevator, elevator_index: int) -> None:
        self.handle_move(alg_elevator, elevator_index)

        alg_elevator.state.position += 1

    def handle_door_open(self, alg_elevator: AlgorithmElevator, elevator_index: int) -> None:
        # Handle drop out
        people_to_drop = self.people_manager.containers[elevator_index].floors[alg_elevator.state.position]
        people_to_drop_ids = list(people_to_drop.keys())
        for person_id in people_to_drop_ids:
            self.people_manager.remove_person(people_to_drop[person_id], elevator_index)
            self.handle_fitness(alg_elevator, 'drop_out')

        # Handle pick up
        people_to_pick = self.people_manager.containers[None].floors[alg_elevator.state.position]
        people_to_pick_ids = list(people_to_pick.keys())
        for person_id in people_to_pick_ids:
            if self.people_manager.containers[elevator_index].count >= self.settings.elevator.elevator_capacity:
                break
            self.people_manager.move_person(people_to_pick[person_id], None, elevator_index)
            self.handle_fitness(alg_elevator, 'pick_up')

        # Handle door movement
        if (len(people_to_drop_ids) + len(people_to_pick_ids)) == 0:
            self.handle_fitness(alg_elevator, 'useless_door_movement')
        else:
            self.handle_fitness(alg_elevator, 'door_movement')

    def evaluate_elevator_move(self, alg_elevator: AlgorithmElevator, elevator_index: int, move_index: int) -> None:
        move = alg_elevator.state.path[move_index]
        handler = self.move_handlers.get(move)
        handler(alg_elevator, elevator_index)

        # Handle journey time fitness
        self.handle_fitness(alg_elevator, 'journey_time', self.people_manager.containers[elevator_index].count)

    def evaluate_move(self, member: Member, move_index: int) -> None:
        for elevator_index, alg_elevator in enumerate(member.elevators):
            self.evaluate_elevator_move(alg_elevator, elevator_index, move_index)

        # Handle waiting time fitness
        member.fitness += self.settings.fitness.waiting_time * self.people_manager.containers[None].count

    @staticmethod
    def reset_fitness(member: Member) -> None:
        for elevator in member.elevators:
            elevator.fitness = 0
        member.fitness = 0

    def evaluate(self, member: Member) -> None:
        self.reset_fitness(member)

        original_positions_of_elevators = [elevator.state.position for elevator in member.elevators]
        for move_index in range(self.settings.path.path_length):
            self.evaluate_move(member, move_index)

        for elevator in member.elevators:
            member.fitness += elevator.fitness

        # Rollback
        self.people_manager.rollback()
        for elevator_index, position in enumerate(original_positions_of_elevators):
            member.elevators[elevator_index].state.position = position
