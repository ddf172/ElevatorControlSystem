from app.src.Managers.EvaluatorPeopleManager import EvaluatorPeopleManager
from app.src.Managers.SystemPeopleManager import SystemPeopleManager
from app.src.Managers.PeopleManager import PeopleContainer
from app.src.Objects.Person import AlgorithmPerson, Person
from typing import Union, Dict


def _convert_person(person: Person, where: Union[None, int]) -> AlgorithmPerson:
    return AlgorithmPerson(
        start_pos=person.start_pos,
        destination=person.destination,
        current_affiliation=where,
        original_affiliation=where,
        person_id=person.id
    )


def _convert_floor(people: Dict[int, Person], where: Union[None, int], floor: int,
                   evaluator_manager: EvaluatorPeopleManager) -> None:
    for person in people.values():
        algorithm_person = _convert_person(person, where)
        evaluator_manager.add_person(algorithm_person, where, floor)


def _convert_container(container: PeopleContainer, where: Union[None, int],
                       evaluator_manager: EvaluatorPeopleManager) -> None:
    for floor, people in container.floors.items():
        _convert_floor(people, where, floor, evaluator_manager)


def convert(system_manager: SystemPeopleManager) -> EvaluatorPeopleManager:
    evaluator_manager = EvaluatorPeopleManager()

    for where, container in system_manager.containers.items():
        _convert_container(container, where, evaluator_manager)

    return evaluator_manager
