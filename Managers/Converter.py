from Managers.EvaluatorPeopleManager import EvaluatorPeopleManager
from Managers.SystemPeopleManager import SystemPeopleManager
from Objects.Person import AlgorithmPerson, Person
from typing import Union


class SystemToEvaluatorConverter:
    @staticmethod
    def _convert_to_algorithm_person(person: Person, elevator_index: Union[None, int]) -> AlgorithmPerson:
        return AlgorithmPerson(person.start_pos, person.destination, elevator_index)

    @staticmethod
    def _adapt_object_people(evaluator_manager: EvaluatorPeopleManager, container: dict, elevator_index: Union[None, int]):
        for floor, floor_people in container.items():
            for person in floor_people.values():
                algorithm_person = SystemToEvaluatorConverter._convert_to_algorithm_person(person, elevator_index)
                evaluator_manager.add_person(algorithm_person, elevator_index)

    @staticmethod
    def _adapt_waiting_people(system_manager: SystemPeopleManager, evaluator_manager: EvaluatorPeopleManager):
        SystemToEvaluatorConverter._adapt_object_people(evaluator_manager, system_manager.waiting_people, None)

    @staticmethod
    def _adapt_elevator_people(system_manager: SystemPeopleManager, evaluator_manager: EvaluatorPeopleManager):
        for elevator_index, elevator in enumerate(system_manager.elevator_people):
            SystemToEvaluatorConverter._adapt_object_people(evaluator_manager, elevator, elevator_index)

    @staticmethod
    def adapt(system_manager: SystemPeopleManager) -> EvaluatorPeopleManager:
        evaluator_manager = EvaluatorPeopleManager()
        SystemToEvaluatorConverter._adapt_waiting_people(system_manager, evaluator_manager)
        SystemToEvaluatorConverter._adapt_elevator_people(system_manager, evaluator_manager)
        return evaluator_manager
