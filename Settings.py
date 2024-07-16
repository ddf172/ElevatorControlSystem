from Singleton import Singleton


class Settings(Singleton):

    def __init__(self):
        if hasattr(self, 'initialized'): return
        self.initialized = True

        self._elevator_number = 3

        self._lowest_floor = 0
        self._highest_floor = 10

        # Tabu
        self._path_length = 10
        self.move_possibilities = [-1, 0, 1, 2]
        self.path_possible_moves = {
            "bottom_floor": [0, 1, 2],
            "top_floor": [-1, 0, 2],
            -1: [-1, 2],
            0: [-1, 0, 1, 2],
            1: [1, 2],
            2: [-1, 0, 1],
        }

    def get_path_length(self):
        return self._path_length

    def get_elevator_number(self):
        return self._elevator_number

    def get_lowest_floor(self):
        return self._lowest_floor

    def get_highest_floor(self):
        return self._highest_floor
