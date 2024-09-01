import pytest
from Algorithm.Tabu import Tabu, Floor
from Settings.Settings import Settings
from Objects.PathState import PathState
from unittest.mock import patch


@pytest.fixture
def tabu():
    return Tabu([])


@pytest.fixture
def settings():
    return Settings()


def test_init(tabu, settings):
    assert isinstance(tabu.settings, Settings)
    assert isinstance(tabu.state, PathState)
    assert tabu.state.path == []
    assert tabu.state.position == 0
    assert tabu.state.last_move_from_prev_iteration == 0


def test_append_move(tabu):
    tabu.append_move(1)
    assert tabu.state.path == [1]
    assert tabu.state.position == 1

    tabu.append_move(2)
    assert tabu.state.path == [1, 2]
    assert tabu.state.position == 1

    tabu.append_move(0)
    assert tabu.state.path == [1, 2, 0]
    assert tabu.state.position == 1

    tabu.append_move(-1)
    assert tabu.state.path == [1, 2, 0, -1]
    assert tabu.state.position == 0


def test_get_proper_key(tabu, settings):
    assert tabu.get_proper_key(settings.get_lowest_floor(), -1) == Floor.BOTTOM.value
    assert tabu.get_proper_key(settings.get_highest_floor(), 2) == Floor.TOP.value
    assert tabu.get_proper_key(3, 1) == 1
    assert tabu.get_proper_key(3, 2) == 2
    assert tabu.get_proper_key(3, 0) == 0
    assert tabu.get_proper_key(3, -1) == -1


def test_get_possible_moves(tabu, settings):
    assert tabu._get_possible_moves(Floor.BOTTOM.value, -1) == [2]
    assert tabu._get_possible_moves(Floor.TOP.value, 1) == [2]
    assert tabu._get_possible_moves(Floor.BOTTOM.value, 2) == settings.path.path_possible_moves[Floor.BOTTOM.value]
    assert tabu._get_possible_moves(1, 1) == settings.path.path_possible_moves[1]
    assert tabu._get_possible_moves(2, 1) == settings.path.path_possible_moves[2]
    assert tabu._get_possible_moves(0, 1) == settings.path.path_possible_moves[0]
    assert tabu._get_possible_moves(-1, 1) == settings.path.path_possible_moves[-1]


def test_get_valid_move_list(tabu, settings):
    assert tabu.get_valid_move_list(0, settings.get_lowest_floor()) == settings.path.path_possible_moves[Floor.BOTTOM.value]
    assert tabu.get_valid_move_list(1, 5) == [1, 2]
    assert tabu.get_valid_move_list(2, settings.get_highest_floor()) == settings.path.path_possible_moves[Floor.TOP.value]
    assert tabu.get_valid_move_list(-1, 5) == [-1, 2]
    assert tabu.get_valid_move_list(0, 5) == settings.path.path_possible_moves[0]

    with pytest.raises(ValueError):
        tabu.get_valid_move_list(3, 5)  # 3 is not a valid move


def test_generate_single_move(tabu):
    assert tabu.generate_single_move(0, 0) in tabu.get_valid_move_list(0, 0)
    assert tabu.generate_single_move(1, 5) in tabu.get_valid_move_list(1, 5)
    assert tabu.generate_single_move(2, 5) in tabu.get_valid_move_list(2, 5)
    assert tabu.generate_single_move(-1, 5) in tabu.get_valid_move_list(-1, 5)
    assert tabu.generate_single_move(0, 5) in tabu.get_valid_move_list(0, 5)

    moves = set(tabu.generate_single_move(0, 2) for _ in range(10))
    assert len(moves) > 1, "The function seems to always return the same move"


def test_get_previous_move(tabu):
    tabu.state.path = [1, 2, -1]
    assert tabu.get_previous_move() == -1

    tabu.state.path = []
    tabu.state.last_move_from_prev_iteration = 2
    assert tabu.get_previous_move() == 2

    tabu.state.path = [1]
    tabu.state.last_move_from_prev_iteration = 2
    assert tabu.get_previous_move() == 1


def generate_path(tabu, position, last_move):
    tabu.state.position = position
    tabu.state.last_move_from_prev_iteration = last_move
    return tabu.generate_new_path()


def verify_path(tabu, settings, position, last_move, expected_position, path, path_length=10):

    assert len(path) == path_length, "Path length mismatch."
    for move in path:
        assert move in tabu.get_valid_move_list(last_move, position), f"Invalid move {move} from position {position}."
        last_move = move
        if move <= 1:
            position += move
    assert tabu.state.position == expected_position, f"Position mismatch. Expected: {expected_position}, but got: {tabu.state.position}."


def test_generate_new_path(tabu, settings):
    # Test #1
    path = generate_path(tabu, 0, 0)
    verify_path(tabu, settings, position=0, last_move=0, expected_position=0, path=path)

    # Test #2
    path = generate_path(tabu, 5, 1)
    verify_path(tabu, settings, position=5, last_move=1, expected_position=5, path=path)

    # Test #3
    path = generate_path(tabu, settings.get_highest_floor(), 1)
    verify_path(tabu, settings, position=settings.get_highest_floor(), last_move=1,
                           expected_position=settings.get_highest_floor(), path=path)


def test_get_repaired_move(tabu, settings):
    assert tabu.get_repaired_move(0, 1, 1) == 1
    assert tabu.get_repaired_move(-1, 1, 1) in [-1, 2]
    assert tabu.get_repaired_move(1, 1, 1) == 1
    assert tabu.get_repaired_move(2, 1, 1) == 1
    assert tabu.get_repaired_move(0, -1, settings.get_lowest_floor()) in settings.path.path_possible_moves[Floor.BOTTOM.value]
    assert tabu.get_repaired_move(0, 0, 0) == 0
    assert tabu.get_repaired_move(1, 1, settings.get_highest_floor()) == 2

    with pytest.raises(ValueError):
        tabu.get_repaired_move(0, 1, settings.get_lowest_floor() - 1)
    with pytest.raises(ValueError):
        tabu.get_repaired_move(0, 1, settings.get_highest_floor() + 1)


def test_validate_and_repair_path(tabu, settings):
    tabu.state.path = [1, 2, 1, 3, 1, 0, 0, 1, -1, 0]  # 3 is invalid
    tabu.validate_and_repair_path()
    verify_path(tabu, settings, position=0, last_move=0, expected_position=0, path=tabu.state.path)


def test_validate_and_repair_path_start_index(tabu, settings):
    tabu.state.path = [1, 2, 1, 3, 1, 0, 0, 1, -1, 0]
    tabu.validate_and_repair_path(start_index=3)
    verify_path(tabu, settings, position=0, last_move=0, expected_position=0, path=tabu.state.path)

    tabu.state.path = [1, 2, 1, 3, 1, 0, 0, 1, -1, 0]
    tabu.validate_and_repair_path(start_index=5)
    assert tabu.state.path[3] == 3, f"Expected value at index 4 to be 3, but got {tabu.state.path[3]}"
    verify_path(tabu, settings, position=0, last_move=0, expected_position=0, path=tabu.state.path[5:], path_length=5)


def test_get_path(tabu):
    tabu.state.path = [1, 2, 3]
    assert tabu.get_path() == [1, 2, 3]
