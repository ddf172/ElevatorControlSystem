import pytest
from src.Algorithm.MemberEvaluator import MemberEvaluator
from src.Objects.Member import Member
from src.Objects.Elevator import AlgorithmElevator


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
