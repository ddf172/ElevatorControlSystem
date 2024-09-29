from src.Objects.Elevator import *
from src.Objects.Member import Member
from src.Settings.Settings import Settings
from src.Managers.EvaluatorPeopleManager import EvaluatorPeopleManager
from typing import Dict, Callable


class MemberEvaluator:
    def __init__(self, people_manager: EvaluatorPeopleManager):
        self.people_manager = people_manager
        self.settings = Settings()

        self.move_handlers: Dict[int, Callable[[AlgorithmElevator, int], None]] = {
            -1: self.handle_move_down,
            0: self.handle_no_move,
            1: self.handle_move_up,
            2: self.handle_door_open
        }

    def handle_fitness(self, arg_elevator: AlgorithmElevator, key: str, multiplier: int = 1) -> None:
        arg_elevator.fitness += (self.settings.fitness.__dict__[key])*multiplier

    def handle_move(self, arg_elevator: AlgorithmElevator, elevator_index: int) -> None:
        self.handle_fitness(arg_elevator, 'move_fitness')

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
        self.handle_fitness(alg_elevator, 'door_movement_fitness')

        # Handle drop out
        people_to_drop = self.people_manager.containers[elevator_index].floors[alg_elevator.state.position]
        for person in people_to_drop:
            self.people_manager.remove_person(person, elevator_index)
            self.handle_fitness(alg_elevator, 'drop_out_fitness')

        # Handle pick up
        people_to_pick = self.people_manager.containers[None].floors[alg_elevator.state.position]
        for person in people_to_pick:
            self.people_manager.move_person(person, None, elevator_index)
            self.handle_fitness(alg_elevator, 'pick_up_fitness')

    def evaluate_elevator_move(self, alg_elevator: AlgorithmElevator, elevator_index: int, move_index: int) -> None:
        move = alg_elevator.state.path[move_index]
        handler = self.move_handlers.get(move)
        handler(alg_elevator, elevator_index)

        # Handle journey time fitness
        self.handle_fitness(alg_elevator, 'journey_time', self.people_manager.containers[elevator_index].count)

        # Handle waiting time fitness
        self.handle_fitness(alg_elevator, 'waiting_time', self.people_manager.containers[None].count)

    def evaluate_move(self, member: Member, move_index: int) -> None:
        for elevator_index, alg_elevator in enumerate(member.elevators):
            self.evaluate_elevator_move(alg_elevator, elevator_index, move_index)

    def evaluate(self, member: Member) -> None:
        original_positions_of_elevators = [elevator.state.position for elevator in member.elevators]
        for move_index in range(self.settings.path.path_length):
            self.evaluate_move(member, move_index)

        # Rollback
        self.people_manager.rollback()
        for elevator_index, position in enumerate(original_positions_of_elevators):
            member.elevators[elevator_index].state.position = position
