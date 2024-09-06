import pytest
from Algorithm.Crossover import Crossover
from Settings.Settings import Settings
from Objects.Elevator import AlgorithmElevator
from Objects.Member import Member
from Algorithm.Tabu import Tabu
from random import choice
from Tests.test_Tabu import verify_path


@pytest.fixture
def crossover():
    return Crossover()


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture()
def prepare_crossover_objects():
    elevator1 = AlgorithmElevator(0, 0)
    elevator2 = AlgorithmElevator(0, 0)
    offspring1 = AlgorithmElevator(0, 0)
    offspring2 = AlgorithmElevator(0, 0)
    return elevator1, elevator2, offspring1, offspring2


@pytest.fixture
def tabu():
    return Tabu([], 0, 0)


def prepare_crossover_objects_paths(elevator1, elevator2, offspring1, offspring2, elevator1_path, elevator2_path):
    elevator1.state.path = elevator1_path
    elevator2.state.path = elevator2_path
    offspring1.state.path = []
    offspring2.state.path = []


def get_offspring_path_move_assert(crossover, settings, move1, move2):
    if move1 == move2:
        assert crossover.get_offspring_path_move(move1, move2) == move1
    else:
        assert crossover.get_offspring_path_move(move1, move2) in set(settings.path.path_possible_moves[move1]) - {move1}


def test_get_offspring_path_move_full(crossover, settings):
    get_offspring_path_move_assert(crossover, settings, -1, -1)
    get_offspring_path_move_assert(crossover, settings, 0, 0)
    get_offspring_path_move_assert(crossover, settings, 1, 1)
    get_offspring_path_move_assert(crossover, settings, 2, 2)
    get_offspring_path_move_assert(crossover, settings, -1, 0)
    get_offspring_path_move_assert(crossover, settings, -1, 1)
    get_offspring_path_move_assert(crossover, settings, -1, 2)
    get_offspring_path_move_assert(crossover, settings, 0, -1)
    get_offspring_path_move_assert(crossover, settings, 0, 1)
    get_offspring_path_move_assert(crossover, settings, 0, 2)
    get_offspring_path_move_assert(crossover, settings, 1, -1)
    get_offspring_path_move_assert(crossover, settings, 1, 0)
    get_offspring_path_move_assert(crossover, settings, 1, 2)
    get_offspring_path_move_assert(crossover, settings, 2, -1)
    get_offspring_path_move_assert(crossover, settings, 2, 0)
    get_offspring_path_move_assert(crossover, settings, 2, 1)


def test_append_offspring_elevator_move(crossover, settings, prepare_crossover_objects):
    elevator1, elevator2, offspring1, offspring2 = prepare_crossover_objects

    path1 = [0, 1, 2, 1, 1, 1, 2, -1, -1, 2]
    path2 = [0, 1, 2, 1, 1, 1, 2, -1, -1, 2]
    prepare_crossover_objects_paths(elevator1, elevator2, offspring1, offspring2, path1, path2)

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

    path1 = [1]
    path2 = [0]
    prepare_crossover_objects_paths(elevator1, elevator2, offspring1, offspring2, path1, path2)

    crossover.append_offspring_elevator_move(elevator1, elevator2, offspring1, offspring2, 0)
    assert offspring1.state.path[0] in set(settings.path.path_possible_moves[1]) - {1}
    assert offspring2.state.path[0] in set(settings.path.path_possible_moves[0]) - {0}


def test_crossover_elevators(crossover, settings, prepare_crossover_objects, tabu):
    elevator1, elevator2, offspring1, offspring2 = prepare_crossover_objects

    path1 = [0] * settings.path.path_length
    path2 = [0] * settings.path.path_length
    prepare_crossover_objects_paths(elevator1, elevator2, offspring1, offspring2, path1, path2)

    offspring1, offspring2 = crossover.crossover_elevators(elevator1, elevator2, offspring1, offspring2)
    assert offspring1.state.path == [0] * settings.path.path_length
    assert offspring2.state.path == [0] * settings.path.path_length

    path1 = tabu.generate_new_path()
    path2 = tabu.generate_new_path()
    prepare_crossover_objects_paths(elevator1, elevator2, offspring1, offspring2, path1, path2)

    offspring1, offspring2 = crossover.crossover_elevators(elevator1, elevator2, offspring1, offspring2)

    for i in range(settings.path.path_length):
        if elevator1.state.path[i] == elevator2.state.path[i]:
            assert offspring1.state.path[i] == offspring2.state.path[i] == elevator1.state.path[i]
        else:
            assert offspring1.state.path[i] in set(settings.path.path_possible_moves[path1[i]]) - {path1[i]}
            assert offspring2.state.path[i] in set(settings.path.path_possible_moves[path2[i]]) - {path2[i]}


def test_fix_elevator_path(crossover, tabu, settings):
    elevator = AlgorithmElevator(0, 0)
    elevator.state.path = []
    for _ in range(settings.path.path_length):
        elevator.state.path.append(choice([-1, 0, 1, 2]))

    crossover.fix_elevator_path(elevator)
    verify_path(tabu, settings, elevator.state.position, elevator.state.last_move_from_prev_iteration, elevator.state.position, elevator.state.path, settings.path.path_length)


def test_created_elevator_offspring(crossover, settings, prepare_crossover_objects, tabu):
    elevator1, elevator2, offspring1, offspring2 = prepare_crossover_objects

    path1 = tabu.generate_new_path()
    path2 = tabu.generate_new_path()
    prepare_crossover_objects_paths(elevator1, elevator2, offspring1, offspring2, path1, path2)

    offspring1, offspring2 = crossover.create_elevator_offspring(elevator1, elevator2)

    verify_path(tabu, settings, offspring1.state.position, offspring1.state.last_move_from_prev_iteration, offspring1.state.position, offspring1.state.path, settings.path.path_length)
    verify_path(tabu, settings, offspring2.state.position, offspring2.state.last_move_from_prev_iteration, offspring2.state.position, offspring2.state.path, settings.path.path_length)


def test_crossover_members(crossover, settings, prepare_crossover_objects, tabu):
    parent1 = Member()
    parent2 = Member()
    offspring1 = Member()
    offspring2 = Member()

    for _ in range(settings.elevator.elevator_number):
        elevator1 = AlgorithmElevator(0, 0)
        elevator2 = AlgorithmElevator(0, 0)
        for _ in range(settings.path.path_length):
            elevator1.state.path = tabu.generate_new_path()
            elevator2.state.path = tabu.generate_new_path()
        parent1.add_elevator(elevator1)
        parent2.add_elevator(elevator2)

    offspring1, offspring2 = crossover.crossover_members(parent1, parent2, offspring1, offspring2)

    for i in range(settings.elevator.elevator_number):
        verify_path(tabu, settings, offspring1.elevators[i].state.position, offspring1.elevators[i].state.last_move_from_prev_iteration, offspring1.elevators[i].state.position, offspring1.elevators[i].state.path, settings.path.path_length)
        verify_path(tabu, settings, offspring2.elevators[i].state.position, offspring2.elevators[i].state.last_move_from_prev_iteration, offspring2.elevators[i].state.position, offspring2.elevators[i].state.path, settings.path.path_length)
