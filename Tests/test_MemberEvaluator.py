import pytest
from src.Algorithm.MemberEvaluator import MemberEvaluator
from src.Objects.Member import Member
from src.Objects.Elevator import AlgorithmElevator
from src.Objects.Person import AlgorithmPerson


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
    alg_elevator = AlgorithmElevator(0, 0)
    alg_elevator.state.position = 0

    person1 = AlgorithmPerson(0, 1, 0, 0)
    person2 = AlgorithmPerson(1, 0, 0, 0)
    person3 = AlgorithmPerson(2, 0, 0, 0)

    member_evaluator.people_manager.add_person(person1, 0)
    member_evaluator.people_manager.add_person(person2, 0)
    member_evaluator.people_manager.add_person(person3, 0)

    member_evaluator.handle_move(alg_elevator, 0)

    assert person1.current_affiliation == 0
    assert person2.current_affiliation == 0
    assert person3.current_affiliation == 0
    assert alg_elevator.state.position == 0
    # Two people should be dropped out but elevator missed floor
    proper_fitness = settings.fitness.move + 2 * member_evaluator.settings.fitness.missed_destination_floor
    assert alg_elevator.fitness == proper_fitness


def test_handle_move_down(member_evaluator, settings):
    alg_elevator = AlgorithmElevator(0, 0)
    alg_elevator.state.position = 2

    person1 = AlgorithmPerson(3, 2, 0, 0)
    person2 = AlgorithmPerson(3, 2, 0, 0)
    person3 = AlgorithmPerson(3, 1, 0, 0)

    member_evaluator.people_manager.add_person(person1, 0)
    member_evaluator.people_manager.add_person(person2, 0)
    member_evaluator.people_manager.add_person(person3, 0)

    member_evaluator.handle_move_down(alg_elevator, 0)

    assert person1.current_affiliation == 0
    assert person2.current_affiliation == 0
    assert person3.current_affiliation == 0
    assert alg_elevator.state.position == 1

    # Two people should be dropped out but elevator missed floor
    proper_fitness = settings.fitness.move + 2 * settings.fitness.missed_destination_floor
    assert alg_elevator.fitness == proper_fitness


def test_handle_no_move(member_evaluator, settings):
    alg_elevator = AlgorithmElevator(0, 0)
    alg_elevator.state.position = 0

    person1 = AlgorithmPerson(0, 0, 0, 0)
    person2 = AlgorithmPerson(0, 0, 0, 0)
    person3 = AlgorithmPerson(0, 0, 0, 0)

    member_evaluator.people_manager.add_person(person1, 0)
    member_evaluator.people_manager.add_person(person2, 0)
    member_evaluator.people_manager.add_person(person3, 0)

    member_evaluator.handle_no_move(alg_elevator, 0)

    assert person1.current_affiliation == 0
    assert person2.current_affiliation == 0
    assert person3.current_affiliation == 0
    assert alg_elevator.state.position == 0

    proper_fitness = settings.fitness.no_move + 3 * settings.fitness.no_move_with_passenger
    assert alg_elevator.fitness == proper_fitness


def test_handle_move_up(member_evaluator, settings):
    alg_elevator = AlgorithmElevator(0, 0)
    alg_elevator.state.position = 0

    person1 = AlgorithmPerson(1, 0, 0, 0)
    person2 = AlgorithmPerson(1, 0, 0, 0)
    person3 = AlgorithmPerson(1, 0, 0, 0)

    member_evaluator.people_manager.add_person(person1, 0)
    member_evaluator.people_manager.add_person(person2, 0)
    member_evaluator.people_manager.add_person(person3, 0)

    member_evaluator.handle_move_up(alg_elevator, 0)

    assert person1.current_affiliation == 0
    assert person2.current_affiliation == 0
    assert person3.current_affiliation == 0
    assert alg_elevator.state.position == 1

    proper_fitness = settings.fitness.move + 3 * settings.fitness.missed_destination_floor
    assert alg_elevator.fitness == proper_fitness
