class SettingsPath:
    def __init__(self):
        self.path_length = 10
        self.move_possibilities = [-1, 0, 1, 2]
        self.path_possible_moves = {
            "bottom_floor": [0, 1, 2],
            "top_floor": [-1, 0, 2],
            -1: [-1, 2],
            0: [-1, 0, 1, 2],
            1: [1, 2],
            2: [-1, 0, 1],
        }
        self.lowest_floor = 0
        self.highest_floor = 10


class SettingsFitness:
    def __init__(self):
        self.move = -1
        self.door_movement = -1
        self.no_move = 0
        self.no_move_with_passenger = -10
        self.missed_destination_floor = -100
        self.drop_out = 100
        self.pick_up = 10
        self.waiting_time = -2
        self.journey_time = -1

    def to_dict(self):
        return {
            "move": self.move,
            "door_movement": self.door_movement,
            "no_move": self.no_move,
            "no_move_with_passenger": self.no_move_with_passenger,
            "missed_destination_floor": self.missed_destination_floor,
            "drop_out": self.drop_out,
            "pick_up": self.pick_up,
            "waiting_time": self.waiting_time,
            "journey_time": self.journey_time
        }


class SettingsAlgorithm:
    def __init__(self):
        self.population_size = 200
        self.generations = 50
        self.mutation_rate = 50  # 0 - 1000


class SettingsElevator:
    def __init__(self):
        self.elevator_number = 3
        self.elevator_capacity = 5
