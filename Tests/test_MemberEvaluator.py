import pytest
from src.Algorithm.MemberEvaluator import MemberEvaluator
from src.Objects.Elevator import AlgorithmElevator
from src.Objects.Person import AlgorithmPerson
from src.Objects.Member import Member


def setup_test_scenario(member_evaluator, elevator_position, people_data):
    alg_elevator = AlgorithmElevator(0, 0)
    alg_elevator.state.position = elevator_position

    for person_id, start_floor, destination_floor, current_affiliation, original_affiliation in people_data:
        person = AlgorithmPerson(start_floor, destination_floor, current_affiliation, original_affiliation,
                                 person_id=person_id)
        member_evaluator.people_manager.add_person(person, current_affiliation)

    return alg_elevator


def assert_test_results_for_moves(alg_elevator, member_evaluator, expected_position, expected_fitness,
                                  expected_people_affiliation, container_id):
    assert alg_elevator.state.position == expected_position
    assert alg_elevator.fitness == expected_fitness

    for floor in member_evaluator.people_manager.containers[container_id].floors.values():
        for person in floor.values():
            assert person.current_affiliation == expected_people_affiliation.get(person.id, person.current_affiliation), \
                (f"Mismatch for person {person.id}: expected {expected_people_affiliation.get(person.id)},"
                 f" got {person.current_affiliation}")


@pytest.fixture
def member_evaluator(evaluator_people_manager):
    return MemberEvaluator(evaluator_people_manager)


def test_handle_fitness(member_evaluator, settings):
    alg_elevator = AlgorithmElevator(0, 0)
    key = 'move'
    multiplier = 1
    member_evaluator.handle_fitness(alg_elevator, key, multiplier)
    assert alg_elevator.fitness == settings.fitness.move * multiplier

    alg_elevator.fitness = 0
    key = 'missed_destination_floor'
    multiplier = 2
    member_evaluator.handle_fitness(alg_elevator, key, multiplier)
    assert alg_elevator.fitness == settings.fitness.missed_destination_floor * multiplier


def test_handle_move(member_evaluator, settings):
    people_data = [
        (0, 0, 1, 0, 0),
        (1, 1, 0, 0, 0),
        (2, 2, 0, 0, 0)
    ]
    alg_elevator = setup_test_scenario(member_evaluator, 0, people_data)
    member_evaluator.handle_move(alg_elevator, 0)

    expected_fitness = settings.fitness.move + 2 * settings.fitness.missed_destination_floor
    expected_people_affiliation = {0: 0, 1: 0, 2: 0}
    assert_test_results_for_moves(alg_elevator, member_evaluator, 0, expected_fitness, expected_people_affiliation, 0)


def test_handle_move_down(member_evaluator, settings):
    people_data = [
        (0, 3, 2, 0, 0),
        (1, 3, 2, 0, 0),
        (2, 3, 1, 0, 0)
    ]
    alg_elevator = setup_test_scenario(member_evaluator, 2, people_data)

    member_evaluator.handle_move_down(alg_elevator, 0)

    expected_fitness = settings.fitness.move + 2 * settings.fitness.missed_destination_floor
    expected_people_affiliation = {0: 0, 1: 0, 2: 0}
    assert_test_results_for_moves(alg_elevator, member_evaluator, 1, expected_fitness, expected_people_affiliation, 0)


def test_handle_no_move(member_evaluator, settings):
    people_data = [
        (0, 0, 0, 0, 0),
        (1, 0, 0, 0, 0),
        (2, 0, 0, 0, 0)
    ]
    alg_elevator = setup_test_scenario(member_evaluator, 0, people_data)

    member_evaluator.handle_no_move(alg_elevator, 0)

    expected_fitness = settings.fitness.no_move + 3 * settings.fitness.no_move_with_passenger
    expected_people_affiliation = {0: 0, 1: 0, 2: 0}
    assert_test_results_for_moves(alg_elevator, member_evaluator, 0, expected_fitness, expected_people_affiliation, 0)


def test_handle_move_up(member_evaluator, settings):
    people_data = [
        (0, 1, 0, 0, 0),
        (1, 1, 0, 0, 0),
        (2, 1, 0, 0, 0)
    ]
    alg_elevator = setup_test_scenario(member_evaluator, 0, people_data)

    member_evaluator.handle_move_up(alg_elevator, 0)

    expected_fitness = settings.fitness.move + 3 * settings.fitness.missed_destination_floor
    expected_people_affiliation = {0: 0, 1: 0, 2: 0}
    assert_test_results_for_moves(alg_elevator, member_evaluator, 1, expected_fitness, expected_people_affiliation, 0)


def test_handle_door_open(member_evaluator, settings):
    # people data (person_id, start_floor, destination_floor, current_affiliation, original_affiliation)
    people_data = [
        (0, 0, 0, None, None),
        (1, 0, 0, None, None),
        (2, 0, 0, None, None),
        (3, 1, 0, 0, 0),
        (4, 1, 0, 0, 0),
        (5, 1, 0, 0, 0),
        (6, 2, 1, 0, 0),
        (7, 2, 1, 0, 0),
        (8, 2, 1, 0, 0)
    ]
    alg_elevator = setup_test_scenario(member_evaluator, 0, people_data)
    member_evaluator.handle_door_open(alg_elevator, 0)

    expected_fitness = settings.fitness.door_movement + 3 * settings.fitness.drop_out + 3 * settings.fitness.pick_up
    expected_people_affiliation = {0: 0, 1: 0, 2: 0, 3: -1, 4: -1, 5: -1, 6: 0, 7: 0, 8: 0}
    assert_test_results_for_moves(alg_elevator, member_evaluator, 0, expected_fitness, expected_people_affiliation, 0)


def test_evaluate_elevator_move(member_evaluator, settings):
    people_data = [
        (0, 0, 0, None, None),
        (1, 0, 0, None, None),
        (2, 0, 0, None, None),
        (3, 1, 0, 0, 0),
        (4, 1, 0, 0, 0),
        (5, 1, 0, 0, 0),
        (6, 2, 1, 0, 0),
        (7, 2, 1, 0, 0),
        (8, 2, 1, 0, 0)
    ]
    alg_elevator = setup_test_scenario(member_evaluator, 0, people_data)
    if settings.path.path_length < 5:
        raise ValueError("Test scenario requires path length of at least 5")
    alg_elevator.state.path = [0, 1, 2, -1, 2] + [0] * (settings.path.path_length - 5)

    member_evaluator.evaluate_elevator_move(alg_elevator, 0, 0)

    # No move
    expected_fitness = 0
    expected_fitness += 6 * settings.fitness.no_move_with_passenger
    expected_fitness += 6 * settings.fitness.journey_time + 3 * settings.fitness.waiting_time
    expected_people_affiliation = {0: None, 1: None, 2: None, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

    assert_test_results_for_moves(alg_elevator, member_evaluator, 0, expected_fitness, expected_people_affiliation, 0)

    # Move to the next floor
    member_evaluator.evaluate_elevator_move(alg_elevator, 0, 1)
    expected_fitness += settings.fitness.move + 3 * settings.fitness.missed_destination_floor
    expected_fitness += 6 * settings.fitness.journey_time + 3 * settings.fitness.waiting_time

    assert_test_results_for_moves(alg_elevator, member_evaluator, 1, expected_fitness, expected_people_affiliation, 0)

    # Door open
    member_evaluator.evaluate_elevator_move(alg_elevator, 0, 2)

    expected_people_affiliation = {0: None, 1: None, 2: None, 3: 0, 4: 0, 5: 0, 6: -1, 7: -1, 8: -1}
    expected_fitness += settings.fitness.door_movement + 3 * settings.fitness.drop_out
    expected_fitness += 3 * settings.fitness.waiting_time + 3 * settings.fitness.journey_time
    assert_test_results_for_moves(alg_elevator, member_evaluator, 1, expected_fitness, expected_people_affiliation, 0)

    # Move down
    member_evaluator.evaluate_elevator_move(alg_elevator, 0, 3)

    expected_fitness += settings.fitness.move
    expected_fitness += 3 * settings.fitness.journey_time + 3 * settings.fitness.waiting_time
    assert_test_results_for_moves(alg_elevator, member_evaluator, 0, expected_fitness, expected_people_affiliation, 0)

    # Door open
    member_evaluator.evaluate_elevator_move(alg_elevator, 0, 4)

    expected_people_affiliation = {0: 0, 1: 0, 2: 0, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1}
    expected_fitness += settings.fitness.door_movement + 3 * settings.fitness.drop_out
    expected_fitness += 3 * settings.fitness.pick_up + 3 * settings.fitness.journey_time
    assert_test_results_for_moves(alg_elevator, member_evaluator, 0, expected_fitness, expected_people_affiliation, 0)

    removed_count = 0
    for person in member_evaluator.people_manager.moved_elevator_people:
        if person.current_affiliation == -1:
            removed_count += 1
    assert removed_count == 6


# def test_evaluate_move(member_evaluator, settings):
#     # Store initial settings
#     initial_path_length = settings.path.path_length
#     initial_elevator_number = settings.elevator.elevator_number
#     initial_elevator_capacity = settings.elevator.elevator_capacity
#     initial_lowest_floor = settings.path.lowest_floor
#     initial_highest_floor = settings.path.highest_floor
#
#     # Set new settings
#     settings.path.path_length = 5
#     settings.elevator.elevator_number = 2
#     settings.elevator.elevator_capacity = 5
#     settings.path.lowest_floor = 0
#     settings.path.highest_floor = 5
#
#     # Setup member
#     member = Member()
#     alg_elevator1 = AlgorithmElevator(0, 0)
#     alg_elevator2 = AlgorithmElevator(2, 0)
#     alg_elevator1.state.path = [0, 1, 2, -1, 2]
#     alg_elevator2.state.path = [2, -1, 2, 0, 0]
#     member.add_elevator(alg_elevator1)
#     member.add_elevator(alg_elevator2)
#
#     # Setup people
#     people_data = [
#         (0, 0, 0, None, None),
#         (1, 0, 0, None, None),
#         (2, 0, 0, None, None),
#         (3, 1, 0, 0, 0),
#         (4, 1, 0, 0, 0),
#         (5, 1, 0, 0, 0),
#         (6, 2, 1, None, None),
#         (7, 4, 1, 1, 1),
#         (8, 3, 2, 1, 1)
#     ]
#
#     for person_id, start_floor, destination_floor, current_affiliation, original_affiliation in people_data:
#         person = AlgorithmPerson(start_floor, destination_floor, current_affiliation, original_affiliation, person_id=person_id)
#         member_evaluator.people_manager.add_person(person, current_affiliation)
#
#     # Move 1
#     member_evaluator.evaluate_move(member, 0)
#
#     # Revert settings
#     settings.path.path_length = initial_path_length
#     settings.elevator.elevator_number = initial_elevator_number
#     settings.elevator.elevator_capacity = initial_elevator_capacity
#     settings.path.lowest_floor = initial_lowest_floor
#     settings.path.highest_floor = initial_highest_floor
#
#
#
#
# # TODO Make test that tests if there is capacity overflow in elevators