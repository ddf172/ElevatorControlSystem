import pytest
from Algorithm.Crossover import Crossover
from Settings.Settings import Settings
from Objects.Elevator import AlgorithmElevator


@pytest.fixture
def crossover():
    return Crossover()


@pytest.fixture
def settings():
    return Settings()


def test_get_offspring_path_move(crossover, settings):
    assert crossover.get_offspring_path_move(0, 0) == 0
    assert crossover.get_offspring_path_move(1, 1) == 1
    assert crossover.get_offspring_path_move(2, 2) == 2
    assert crossover.get_offspring_path_move(-1, -1) == -1
    assert crossover.get_offspring_path_move(-1, 0) in set(settings.path.path_possible_moves[-1]) - {-1}
    assert crossover.get_offspring_path_move(-1, 1) in set(settings.path.path_possible_moves[-1]) - {-1}
    assert crossover.get_offspring_path_move(-1, 2) in set(settings.path.path_possible_moves[-1]) - {-1}
    assert crossover.get_offspring_path_move(0, -1) in set(settings.path.path_possible_moves[0]) - {0}
    assert crossover.get_offspring_path_move(0, 1) in set(settings.path.path_possible_moves[0]) - {0}
    assert crossover.get_offspring_path_move(0, 2) in set(settings.path.path_possible_moves[0]) - {0}
    assert crossover.get_offspring_path_move(1, -1) in set(settings.path.path_possible_moves[1]) - {1}
    assert crossover.get_offspring_path_move(1, 0) in set(settings.path.path_possible_moves[1]) - {1}
    assert crossover.get_offspring_path_move(1, 2) in set(settings.path.path_possible_moves[1]) - {1}
    assert crossover.get_offspring_path_move(2, -1) in set(settings.path.path_possible_moves[2]) - {2}
    assert crossover.get_offspring_path_move(2, 0) in set(settings.path.path_possible_moves[2]) - {2}
    assert crossover.get_offspring_path_move(2, 1) in set(settings.path.path_possible_moves[2]) - {2}


def test_append_offspring_elevator_move(crossover, settings):
    elevator1 = AlgorithmElevator(0, 0)
    elevator2 = AlgorithmElevator(0, 0)
    offspring1 = AlgorithmElevator(0, 0)
    offspring2 = AlgorithmElevator(0, 0)

    # Add path to elevators cuz GitHub copilot sucks
    elevator1.state.path = [0, 1, 2, 1, 1, 1, 2, -1, -1, 2]
    elevator2.state.path = [0, 1, 2, 1, 1, 1, 2, -1, -1, 2]

    crossover.append_offspring_elevator_move(elevator1, elevator2, offspring1, offspring2, 0)
    assert offspring1.state.path == [0]
    assert offspring2.state.path == [0]

    crossover.append_offspring_elevator_move(elevator1, elevator2, offspring1, offspring2, 1)
    assert offspring1.state.path == [0, 1]
    assert offspring2.state.path == [0, 1]

    crossover.append_offspring_elevator_move(elevator1, elevator2, offspring1, offspring2, 2)
    assert offspring1.state.path == [0, 1, 2]
    assert offspring2.state.path == [0, 1, 2]

    crossover.append_offspring_elevator_move(elevator1, elevator2, offspring1, offspring2, -1)
    assert offspring1.state.path == [0, 1, 2, 2]
    assert offspring2.state.path == [0, 1, 2, 2]

    elevator1.state.path = [1]
    elevator2.state.path = [0]
    offspring1.state.path = []
    offspring2.state.path = []

    crossover.append_offspring_elevator_move(elevator1, elevator2, offspring1, offspring2, 0)
    assert offspring1.state.path[0] in set(settings.path.path_possible_moves[1]) - {1}
    assert offspring2.state.path[0] in set(settings.path.path_possible_moves[0]) - {0}
