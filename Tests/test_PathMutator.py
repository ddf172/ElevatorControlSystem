# import pytest
# from unittest.mock import patch
# from Algorithm.PathMutator import PathMutator  # Assuming these imports exist
# from Settings.Settings import Settings
# from Objects.Member import Member
# from Objects.Elevator import AlgorithmElevator, Elevator
# from Objects.PathState import PathState
#
#
# # Fixtures
# @pytest.fixture
# def path_mutator():
#     return PathMutator()
#
#
# @pytest.fixture
# def settings():
#     return Settings()
#
#
# @pytest.fixture
# def elevator(settings):
#     return AlgorithmElevator(0)
#
#
# @pytest.fixture
# def member(settings):
#     member = Member()
#     for _ in range(settings.get_elevator_number()):
#         member.add_elevator(AlgorithmElevator(0))
#     return member
#
#
# # Test Functions
# def test_get_move_mutation(path_mutator, settings):
#     for move in settings.path.path_possible_moves:
#         mutated_move = path_mutator.get_move_mutation(move)
#         assert mutated_move in settings.path.path_possible_moves[move]
#         assert mutated_move != move
#
#
# @pytest.mark.parametrize('mock_value', [0, 50])
# def test_mutate_elevator_path(path_mutator, elevator, settings, mock_value):
#     with patch('Algorithm.PathMutator.randint', return_value=mock_value):
#         elevator.state.path = [0] * settings.get_path_length()  # Initialize path
#         original_path = elevator.state.path.copy()
#         path_mutator.mutate_elevator_path(elevator)
#         assert len(elevator.state.path) == len(original_path)
#         assert elevator.state.path != original_path
#
#
# @pytest.mark.parametrize('mock_value', [0, 50])
# def test_mutate_member(path_mutator, member, settings, mock_value):
#     with patch('Algorithm.PathMutator.randint', return_value=mock_value):
#         for elevator in member.elevators:
#             elevator.state.path = [0] * settings.get_path_length()  # Initialize paths
#         original_paths = [elevator.state.path.copy() for elevator in member.elevators]
#         path_mutator.mutate_member(member)
#         for i, elevator in enumerate(member.elevators):
#             assert len(elevator.state.path) == len(original_paths[i])
#             assert elevator.state.path != original_paths[i]
#
#
# @pytest.mark.parametrize('mock_value', [0, 50])
# def test_mutate_population(path_mutator, settings, mock_value):
#     with patch('Algorithm.PathMutator.randint', return_value=mock_value):
#         population = [Member() for _ in range(5)]
#         for member in population:
#             for _ in range(settings.get_elevator_number()):
#                 elevator = AlgorithmElevator(0)
#                 elevator.state.path = [0] * settings.get_path_length()  # Initialize paths
#                 member.add_elevator(elevator)
#
#         original_paths = [[elevator.state.path.copy() for elevator in member.elevators] for member in population]
#         path_mutator.mutate_population(population)
#         for i, member in enumerate(population):
#             for j, elevator in enumerate(member.elevators):
#                 assert len(elevator.state.path) == len(original_paths[i][j])
#                 assert elevator.state.path != original_paths[i][j]
#
#
# def verify_path(settings, position, last_move, path):
#     for move in path:
#         assert move in settings.path.path_possible_moves.get(last_move, settings.path.move_possibilities), \
#             f"Invalid move {move} from last move {last_move}."
#         last_move = move
#         if move <= 1:
#             position += move
#         assert settings.get_lowest_floor() <= position <= settings.get_highest_floor(), \
#             f"Invalid position {position} after move {move}."
#
#
# @pytest.mark.parametrize('mock_value', [0, 50])
# def test_path_integrity_after_mutation(path_mutator, settings, elevator, mock_value):
#     with patch('Algorithm.PathMutator.randint', return_value=mock_value):
#         elevator.state.path = [0] * settings.get_path_length()  # Initialize path
#         path_mutator.mutate_elevator_path(elevator)
#         verify_path(settings, elevator.state.position, elevator.state.last_move_from_prev_iteration, elevator.state.path)
#
#
# @pytest.mark.parametrize('mock_value', [0, 50])
# def test_multiple_mutations(path_mutator, settings, elevator, mock_value):
#     with patch('Algorithm.PathMutator.randint', return_value=mock_value):
#         elevator.state.path = [0] * settings.get_path_length()  # Initialize path
#         path_mutator.mutate_elevator_path(elevator)
#         verify_path(settings, elevator.state.position, elevator.state.last_move_from_prev_iteration, elevator.state.path)
#
#
# # Member Tests
# def test_member_initialization(member, settings):
#     assert len(member.elevators) == settings.get_elevator_number()
#     assert member.fitness == 0
#     assert isinstance(member.settings, Settings)
#
#
# def test_add_elevator(member, settings):
#     with pytest.raises(ValueError):
#         member.add_elevator(AlgorithmElevator(0))
#
#
# def test_add_elevator_wrong_type(settings):
#     member = Member()  # Create a new member without elevators
#     with pytest.raises(TypeError):
#         member.add_elevator("Not an elevator")
#
#
# def test_get_elevator(member):
#     assert isinstance(member.get_elevator(0), AlgorithmElevator)
#     with pytest.raises(IndexError):
#         member.get_elevator(3)
#
#
# # Elevator Tests
# def test_elevator_initialization():
#     elevator = Elevator(5, 1)
#     assert elevator.state.position == 5
#     assert elevator.state.last_move_from_prev_iteration == 1
#     assert elevator.state.path == []
#
#
# def test_algorithm_elevator_initialization():
#     algorithm_elevator = AlgorithmElevator(3, 2)
#     assert algorithm_elevator.state.position == 3
#     assert algorithm_elevator.state.last_move_from_prev_iteration == 2
#     assert algorithm_elevator.state.path == []
#     assert algorithm_elevator.fitness == 0
