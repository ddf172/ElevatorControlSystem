import pytest
from app.src.Algorithm.MemberEvaluator import MemberEvaluator
from app.src.Objects.Elevator import AlgorithmElevator
from app.src.Objects.Person import AlgorithmPerson
from app.src.Objects.Member import Member


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
    return MemberEvaluator(evaluator_people_manager, None)


def member_elevator_with_fixed_settings(evaluator_people_manager, fixed_settings):
    return MemberEvaluator(evaluator_people_manager, fixed_settings)


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


def test_handle_door_open(evaluator_people_manager, settings):
    settings.elevator.elevator_capacity = 5

    member_evaluator = member_elevator_with_fixed_settings(evaluator_people_manager, settings)

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

    # one person won't be picked up because of capacity
    expected_fitness = settings.fitness.door_movement + 3 * settings.fitness.drop_out + 2 * settings.fitness.pick_up
    expected_people_affiliation = {0: 0, 1: 0, 2: None, 3: -1, 4: -1, 5: -1, 6: 0, 7: 0, 8: 0}
    assert_test_results_for_moves(alg_elevator, member_evaluator, 0, expected_fitness, expected_people_affiliation, 0)


def test_evaluate_elevator_move(evaluator_people_manager, settings):
    settings.path.path_length = 5

    member_evaluator = member_elevator_with_fixed_settings(evaluator_people_manager, settings)

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
    alg_elevator.state.path = [0, 1, 2, -1, 2] + [0]

    member_evaluator.evaluate_elevator_move(alg_elevator, 0, 0)

    # No move
    expected_fitness = 0
    expected_fitness += 6 * settings.fitness.no_move_with_passenger
    expected_fitness += 6 * settings.fitness.journey_time
    expected_people_affiliation = {0: None, 1: None, 2: None, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

    assert_test_results_for_moves(alg_elevator, member_evaluator, 0, expected_fitness, expected_people_affiliation, 0)

    # Move to the next floor
    member_evaluator.evaluate_elevator_move(alg_elevator, 0, 1)
    expected_fitness += settings.fitness.move + 3 * settings.fitness.missed_destination_floor
    expected_fitness += 6 * settings.fitness.journey_time

    assert_test_results_for_moves(alg_elevator, member_evaluator, 1, expected_fitness, expected_people_affiliation, 0)

    # Door open
    member_evaluator.evaluate_elevator_move(alg_elevator, 0, 2)

    expected_people_affiliation = {0: None, 1: None, 2: None, 3: 0, 4: 0, 5: 0, 6: -1, 7: -1, 8: -1}
    expected_fitness += settings.fitness.door_movement + 3 * settings.fitness.drop_out
    expected_fitness += 3 * settings.fitness.journey_time
    assert_test_results_for_moves(alg_elevator, member_evaluator, 1, expected_fitness, expected_people_affiliation, 0)

    # Move down
    member_evaluator.evaluate_elevator_move(alg_elevator, 0, 3)

    expected_fitness += settings.fitness.move
    expected_fitness += 3 * settings.fitness.journey_time
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


def test_evaluate_move(evaluator_people_manager, settings):

    # Configure for test
    settings.path.path_length = 5
    settings.elevator.elevator_number = 2
    settings.elevator.elevator_capacity = 5
    settings.path.lowest_floor = 0
    settings.path.highest_floor = 5

    # Setup member
    member = Member()
    alg_elevator0 = AlgorithmElevator(0, 0)
    alg_elevator1 = AlgorithmElevator(2, 0)
    alg_elevator0.state.path = [0, 1, 2, -1, 2]
    alg_elevator1.state.path = [2, -1, 2, 0, 0]
    member.add_elevator(alg_elevator0)
    member.add_elevator(alg_elevator1)

    member_evaluator = member_elevator_with_fixed_settings(evaluator_people_manager, settings)

    # Setup people
    people_data = [
        (0, 0, 0, None, None),
        (1, 0, 0, None, None),
        (2, 0, 0, None, None),
        (3, 1, 0, 0, 0),
        (4, 1, 0, 0, 0),
        (5, 1, 0, 0, 0),
        (6, 2, 1, None, None),
        (7, 4, 1, 1, 1),
        (8, 3, 2, 1, 1)
    ]

    for person_id, start_floor, destination_floor, current_affiliation, original_affiliation in people_data:
        person = AlgorithmPerson(start_floor, destination_floor, current_affiliation, original_affiliation, person_id=person_id)
        member_evaluator.people_manager.add_person(person, current_affiliation)

    # Move 1
    member_evaluator.evaluate_move(member, 0)

    expected_fitness_elevator0 = 0
    expected_fitness_elevator0 += 3 * settings.fitness.no_move_with_passenger + 3 * settings.fitness.journey_time

    expected_fitness_elevator1 = 0
    expected_fitness_elevator1 += settings.fitness.pick_up + settings.fitness.drop_out + settings.fitness.door_movement
    expected_fitness_elevator1 += 2 * settings.fitness.journey_time

    expected_fitness_member = settings.fitness.waiting_time * 3

    expected_people_affiliation = {0: None, 1: None, 2: None, 3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: -1}
    assert_test_results_for_moves(alg_elevator0, member_evaluator, 0, expected_fitness_elevator0, expected_people_affiliation, 0)
    assert_test_results_for_moves(alg_elevator1, member_evaluator, 2, expected_fitness_elevator1, expected_people_affiliation, 1)
    assert member.fitness == expected_fitness_member

    # Move 2
    member_evaluator.evaluate_move(member, 1)

    expected_fitness_elevator0 += settings.fitness.move + 3 * settings.fitness.missed_destination_floor
    expected_fitness_elevator0 += 3 * settings.fitness.journey_time

    expected_fitness_elevator1 += settings.fitness.move + 2 * settings.fitness.journey_time

    expected_fitness_member += settings.fitness.waiting_time * 3

    expected_people_affiliation = {0: None, 1: None, 2: None, 3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: -1}
    assert_test_results_for_moves(alg_elevator0, member_evaluator, 1, expected_fitness_elevator0, expected_people_affiliation, 0)
    assert_test_results_for_moves(alg_elevator1, member_evaluator, 1, expected_fitness_elevator1, expected_people_affiliation, 1)
    assert member.fitness == expected_fitness_member

    # Move 3
    member_evaluator.evaluate_move(member, 2)

    expected_fitness_elevator0 += settings.fitness.door_movement + 3 * settings.fitness.journey_time

    expected_fitness_elevator1 += settings.fitness.door_movement + 2 * settings.fitness.drop_out

    expected_fitness_member += settings.fitness.waiting_time * 3

    expected_people_affiliation = {0: None, 1: None, 2: None, 3: 0, 4: 0, 5: 0, 6: -1, 7: -1, 8: -1}
    assert_test_results_for_moves(alg_elevator0, member_evaluator, 1, expected_fitness_elevator0, expected_people_affiliation, 0)
    assert_test_results_for_moves(alg_elevator1, member_evaluator, 1, expected_fitness_elevator1, expected_people_affiliation, 1)
    assert member.fitness == expected_fitness_member

    # Move 4
    # Elevator 0 position: 1, Elevator 1 position: 1
    member_evaluator.evaluate_move(member, 3)

    expected_fitness_elevator0 += settings.fitness.move
    expected_fitness_elevator0 += 3 * settings.fitness.journey_time

    expected_fitness_elevator1 += settings.fitness.no_move

    expected_fitness_member += settings.fitness.waiting_time * 3

    expected_people_affiliation = {0: None, 1: None, 2: None, 3: 0, 4: 0, 5: 0, 6: -1, 7: -1, 8: -1}
    assert_test_results_for_moves(alg_elevator0, member_evaluator, 0, expected_fitness_elevator0, expected_people_affiliation, 0)
    assert_test_results_for_moves(alg_elevator1, member_evaluator, 1, expected_fitness_elevator1, expected_people_affiliation, 1)
    assert member.fitness == expected_fitness_member

    # Move 5
    member_evaluator.evaluate_move(member, 4)

    expected_fitness_elevator0 += settings.fitness.door_movement + 3 * settings.fitness.drop_out
    expected_fitness_elevator0 += 3 * settings.fitness.pick_up + 3 * settings.fitness.journey_time

    expected_fitness_elevator1 += settings.fitness.no_move

    expected_people_affiliation = {0: 0, 1: 0, 2: 0, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1}
    assert_test_results_for_moves(alg_elevator0, member_evaluator, 0, expected_fitness_elevator0, expected_people_affiliation, 0)
    assert_test_results_for_moves(alg_elevator1, member_evaluator, 1, expected_fitness_elevator1, expected_people_affiliation, 1)
    assert member.fitness == expected_fitness_member


def test_evaluate(evaluator_people_manager, settings):

    # Configure for test
    settings.path.path_length = 5
    settings.elevator.elevator_number = 2
    settings.elevator.elevator_capacity = 5
    settings.path.lowest_floor = 0
    settings.path.highest_floor = 5

    member_evaluator = member_elevator_with_fixed_settings(evaluator_people_manager, settings)

    # Setup member
    member = Member()
    alg_elevator0 = AlgorithmElevator(0, 0)
    alg_elevator1 = AlgorithmElevator(2, 0)
    alg_elevator0.state.path = [0, 1, 2, -1, 2]
    alg_elevator1.state.path = [2, -1, 2, 0, 0]
    member.add_elevator(alg_elevator0)
    member.add_elevator(alg_elevator1)

    # Setup people
    people_data = [
        (0, 0, 0, None, None),
        (1, 0, 0, None, None),
        (2, 0, 0, None, None),
        (3, 1, 0, 0, 0),
        (4, 1, 0, 0, 0),
        (5, 1, 0, 0, 0),
        (6, 2, 1, None, None),
        (7, 4, 1, 1, 1),
        (8, 3, 2, 1, 1)
    ]

    for person_id, start_floor, destination_floor, current_affiliation, original_affiliation in people_data:
        person = AlgorithmPerson(start_floor, destination_floor, current_affiliation, original_affiliation, person_id=person_id)
        member_evaluator.people_manager.add_person(person, current_affiliation)

    member_evaluator.evaluate(member)

    expected_fitness_elevator0 = 0
    expected_fitness_elevator1 = 0
    expected_fitness_member = 0

    expected_fitness_elevator0 += 2 * settings.fitness.door_movement
    expected_fitness_elevator0 += 15 * settings.fitness.journey_time
    expected_fitness_elevator0 += 3 * settings.fitness.no_move_with_passenger
    expected_fitness_elevator0 += 2 * settings.fitness.move
    expected_fitness_elevator0 += 3 * settings.fitness.missed_destination_floor
    expected_fitness_elevator0 += 3 * settings.fitness.drop_out
    expected_fitness_elevator0 += 3 * settings.fitness.pick_up

    expected_fitness_elevator1 += 2 * settings.fitness.door_movement
    expected_fitness_elevator1 += 4 * settings.fitness.journey_time
    expected_fitness_elevator1 += 1 * settings.fitness.pick_up
    expected_fitness_elevator1 += 3 * settings.fitness.drop_out
    expected_fitness_elevator1 += settings.fitness.move
    expected_fitness_elevator1 += 2 * settings.fitness.no_move

    expected_fitness_member += 12 * settings.fitness.waiting_time

    expected_people_affiliation = {0: None, 1: None, 2: None, 3: 0, 4: 0, 5: 0, 6: None, 7: 1, 8: 1}

    assert_test_results_for_moves(alg_elevator0, member_evaluator, 0, expected_fitness_elevator0, expected_people_affiliation, 0)
    assert_test_results_for_moves(alg_elevator1, member_evaluator, 2, expected_fitness_elevator1, expected_people_affiliation, 1)
    assert member.fitness == expected_fitness_member
