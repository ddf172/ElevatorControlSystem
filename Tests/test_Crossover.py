import pytest
from Algorithm.Crossover import Crossover
from Settings.Settings import Settings


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


