from Managers.EvaluatorPeopleManager import EvaluatorPeopleManager
from Managers.SystemPeopleManager import SystemPeopleManager
from Managers.PeopleManager import PeopleContainer
from Objects.Person import AlgorithmPerson, Person
from typing import Union, Dict


class SystemToEvaluatorConverter:
    @staticmethod
    def _convert_person(person: Person, where: Union[None, int]) -> AlgorithmPerson:
        return AlgorithmPerson(
            start_pos=person.start_pos,
            destination=person.destination,
            current_affiliation=where,
            original_affiliation=where
        )

    @staticmethod
    def _convert_floor(people: Dict[int, Person], where: Union[None, int], floor: int,
                       evaluator_manager: EvaluatorPeopleManager) -> None:
        for person in people.values():
            algorithm_person = SystemToEvaluatorConverter._convert_person(person, where)
            evaluator_manager.add_person(algorithm_person, where, floor)

    @staticmethod
    def _convert_container(container: PeopleContainer, where: Union[None, int],
                           evaluator_manager: EvaluatorPeopleManager) -> None:
        for floor, people in container.floors.items():
            SystemToEvaluatorConverter._convert_floor(people, where, floor, evaluator_manager)

    @staticmethod
    def convert(system_manager: SystemPeopleManager) -> EvaluatorPeopleManager:
        evaluator_manager = EvaluatorPeopleManager()

        for where, container in system_manager.containers.items():
            SystemToEvaluatorConverter._convert_container(container, where, evaluator_manager)

        return evaluator_manager
