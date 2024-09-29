from src.Objects.PathState import PathState


class Elevator:
    def __init__(self, position, last_move=0):
        self.state = PathState([], position, last_move)


class SystemElevator(Elevator):
    def __init__(self, position, last_move=0):
        super().__init__(position, last_move)


class AlgorithmElevator(Elevator):
    def __init__(self, position, last_move=0):
        super().__init__(position, last_move)
        self.fitness = 0
