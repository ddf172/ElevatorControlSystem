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
        # Fitness
        self.move_penalty = -1
        self.door_movement = -1
        self.no_move = 0
        self.no_move_with_passenger = -10
        self.missed_destination_floor = -100
        self.drop_out = 100
        self.pick_up = 10
        self.waiting_time = -2
        self.journey_time = -1

        # Algorithm configuration
        self.population_size = 200
        self.generations = 50
        self.mutation_rate = 50  # 0 - 1000
        self.mutation_amount = 2
        self.path_length = 10

    def get_path_length(self):
        return self._path_length

    def get_elevator_number(self):
        return self._elevator_number

    def get_lowest_floor(self):
        return self._lowest_floor

    def get_highest_floor(self):
        return self._highest_floor
