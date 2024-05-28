from Settings import Settings
from random import choice


class Tabu:
    move_possibilities = [-1, 0, 1, 2]
    path_possible_moves = {
        "bottom_floor": [0, 1, 2],
        "top_floor": [-1, 0, 1],
        -1: [-1, 2],
        0: [-1, 0, 1, 2],
        1: [1, 2],
        2: [-1, 0, 1],
    }

    def __init__(self, path, position=0, last_move=0):
        self.settings = Settings()
        if path is None:
            path = []
        self.path = path
        self.original_position = position
        self.curr_position = position
        self.last_move_from_previous_iteration = last_move
        self.path_length = self.settings.get_path_length()

    def get_random_valid_move(self, prev_move, curr_floor):
        if curr_floor == self.settings.get_lowest_floor():
            possible_moves = set(self.path_possible_moves["bottom_floor"])
        elif curr_floor == self.settings.get_highest_floor():
            possible_moves = set(self.path_possible_moves["top_floor"])
        else:
            possible_moves = set(self.path_possible_moves[prev_move])

        return choice(list(possible_moves))

    def get_valid_move(self, prev_move, move, curr_floor):
        if curr_floor == self.settings.get_lowest_floor():
            possible_moves = set(self.path_possible_moves["bottom_floor"])
        elif curr_floor == self.settings.get_highest_floor():
            possible_moves = set(self.path_possible_moves["top_floor"])
        else:
            possible_moves = set(self.path_possible_moves[prev_move])

        possible_moves.discard(move)

        if not possible_moves:
            raise (ValueError("No possible moves"))

        return choice(list(possible_moves))

    def append_move(self, move):
        self.path.append(move)

    def generate_move(self):
        if len(self.path) == self.path_length:
            raise (ValueError("Path already generated"))

        if not self.path:
            prev_move = self.last_move_from_previous_iteration
        else:
            prev_move = self.path[-1]
        move = self.get_random_valid_move(prev_move, self.curr_position)
        return move

    def generate_path(self):
        for i in range(self.path_length):
            move = self.generate_move()
            self.append_move(move)
            if self.path[-1] <= 1:
                self.curr_position += self.path[-1]

    def change_move(self, index, move):  # Can breach the floor limits
        if index < 0 or index >= self.path_length:
            raise (IndexError("Index out of range"))
        if index == 0:
            if move not in self.path_possible_moves[self.last_move_from_previous_iteration]:
                raise (ValueError("Tabu violation"))
        else:
            if move not in self.path_possible_moves[self.path[index - 1]]:
                raise (ValueError("Tabu violation"))
        self.path[index] = move

    def validate_path(self):
        if len(self.path) == 0 or len(self.path) != self.path_length:
            raise (ValueError("Path not generated"))

        curr_floor = self.original_position
        for i in range(self.path_length):
            if i == 0:
                valid_moves = self.path_possible_moves[self.last_move_from_previous_iteration]
                if self.path[i] not in valid_moves:
                    self.path[i] = self.change_move(i, self.get_valid_move(self.last_move_from_previous_iteration, self.path[i], curr_floor))

            else:
                valid_moves = self.path_possible_moves[self.path[i - 1]]
                if self.path[i] not in valid_moves:
                    self.path[i] = self.change_move(i, self.get_valid_move(self.path[i - 1], self.path[i], curr_floor))

            if self.path[i] <= 1:
                curr_floor += self.path[i]
        self.curr_position = curr_floor

    def get_path(self):
        return self.path
