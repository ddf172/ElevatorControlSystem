from Settings import Settings
from random import choice
from enum import Enum
from typing import List, Union
from Objects import PathState


class Floor(Enum):
    BOTTOM = "bottom_floor"
    TOP = "top_floor"


class Tabu:

    def __init__(self, path: List[int], position: int = 0, last_move: int = 0):
        self.settings = Settings()
        self.state = PathState(path or [], position, last_move)

    def append_move(self, move: int) -> None:
        self.state.path.append(move)
        if move <= 1:
            self.state.curr_position += move

    def get_proper_key(self, curr_floor: int, prev_move: int) -> Union[Floor, int]:
        if curr_floor == self.settings.get_lowest_floor():
            key = Floor.BOTTOM.value
        elif curr_floor == self.settings.get_highest_floor():
            key = Floor.TOP.value
        else:
            key = prev_move

        return key

    def get_possible_moves(self, key: Union[Floor, int]) -> List[int]:
        return self.settings.path.path_possible_moves.get(key)

    def get_valid_move_list(self, prev_move: int, curr_floor: int) -> List[int]:
        possible_moves = self.get_possible_moves(self.get_proper_key(curr_floor, prev_move))

        if not possible_moves:
            raise ValueError(f"No valid moves for: floor={curr_floor}, prev_move={prev_move}")

        return possible_moves

    def generate_single_move(self, prev_move: int, curr_position: int) -> int:
        if len(self.state.path) == self.settings.get_path_length():
            raise ValueError("Path is already generated")
        possible_moves = self.get_valid_move_list(prev_move, curr_position)

        return choice(possible_moves)

    def generate_new_path(self) -> List[int]:
        self.state.path = []
        self.state.curr_position = self.state.original_position
        for _ in range(self.settings.get_path_length()):
            if not self.state.path:
                prev_move = self.state.last_move_from_prev_iteration
            else:
                prev_move = self.state.path[-1]
            move = self.generate_single_move(prev_move, self.state.curr_position)

            self.append_move(move)

        return self.state.path

    def get_repaired_move(self, prev_move: int, move: int, curr_floor: int) -> int:
        if curr_floor <= self.settings.get_lowest_floor()-1 or curr_floor >= self.settings.get_highest_floor() + 1:
            raise ValueError(f"Invalid floor: {curr_floor}, not possible to repair")

        possible_moves = self.get_possible_moves(self.get_proper_key(curr_floor, prev_move))
        if move in possible_moves:
            return move
        return choice(possible_moves)

    def validate_and_repair_path(self) -> None:
        if not self.state.path:
            return
        prev_move = self.state.last_move_from_prev_iteration
        curr_floor = self.state.original_position
        for index, move in enumerate(self.state.path):
            self.state.path[index] = self.get_repaired_move(prev_move, move, curr_floor)
            if self.state.path[index] <= 1:
                curr_floor += self.state.path[index]
            prev_move = self.state.path[index]

    def get_path(self) -> List[int]:
        return self.state.path
