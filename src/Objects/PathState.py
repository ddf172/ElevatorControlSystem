from typing import List


class PathState:
    def __init__(self, path: List[int], position: int = 0, last_move: int = 0):
        self.path = path
        self.position = position
        self.last_move_from_prev_iteration = last_move
