from Settings.Settings import Settings
from random import choice
from enum import Enum
from typing import List, Union
from Objects.PathState import PathState


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
            self.state.position += move

    def get_proper_key(self, curr_floor: int, prev_move: int) -> Union[Floor, int]:
        if curr_floor == self.settings.get_lowest_floor():
            key = Floor.BOTTOM.value
        elif curr_floor == self.settings.get_highest_floor():
            key = Floor.TOP.value
        else:
            key = prev_move

        return key

    def _get_possible_moves(self, key: Union[Floor, int], prev_move) -> List[int]:
        if key == Floor.BOTTOM.value and prev_move == -1:
            return [2]
        if key == Floor.TOP.value and prev_move == 1:
            return [2]
        return self.settings.path.path_possible_moves.get(key)

    def get_valid_move_list(self, prev_move: int, curr_floor: int) -> List[int]:
        possible_moves = self._get_possible_moves(self.get_proper_key(curr_floor, prev_move), prev_move)

        if not possible_moves:
            raise ValueError(f"No valid moves for: floor={curr_floor}, prev_move={prev_move}")

        return possible_moves

    def generate_single_move(self, prev_move: int, curr_position: int) -> int:
        if len(self.state.path) == self.settings.get_path_length():
            raise ValueError("Path is already generated")
        possible_moves = self.get_valid_move_list(prev_move, curr_position)

        return choice(possible_moves)

    def get_previous_move(self) -> int:
        return self.state.path[-1] if self.state.path else self.state.last_move_from_prev_iteration

    def generate_new_path(self) -> List[int]:
        self.state.path = []
        original_position = self.state.position
        for _ in range(self.settings.get_path_length()):
            prev_move = self.get_previous_move()
            move = self.generate_single_move(prev_move, self.state.position)

            self.append_move(move)

        self.state.position = original_position
        return self.state.path

    def get_repaired_move(self, prev_move: int, move: int, curr_floor: int) -> int:
        if curr_floor <= self.settings.get_lowest_floor()-1 or curr_floor >= self.settings.get_highest_floor() + 1:
            raise ValueError(f"Invalid floor: {curr_floor}, not possible to repair")

        possible_moves = self.get_valid_move_list(prev_move, curr_floor)
        if move in possible_moves:
            return move
        return choice(possible_moves)

    def validate_and_repair_path(self, start_index: int = 0) -> None:
        if not self.state.path:
            return
        original_position = self.state.position

        self.state.position += sum(move for move in self.state.path[:start_index] if move <= 1)

        if start_index == 0:
            prev_move = self.state.last_move_from_prev_iteration
        else:
            prev_move = self.state.path[start_index - 1]

        for index, move in enumerate(self.state.path[start_index:], start=start_index):
            self.state.path[index] = self.get_repaired_move(prev_move, move, self.state.position)
            if self.state.path[index] <= 1:
                self.state.position += self.state.path[index]
            prev_move = self.state.path[index]

        self.state.position = original_position

    def get_path(self) -> List[int]:
        return self.state.path
