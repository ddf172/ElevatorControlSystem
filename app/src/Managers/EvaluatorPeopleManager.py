from app.src.Managers.PeopleManager import PeopleManager
from app.src.Objects.Person import AlgorithmPerson
from typing import Union


class EvaluatorPeopleManager(PeopleManager[AlgorithmPerson]):
    def __init__(self):
        super().__init__()
        self.moved_elevator_people = set()

    def add_person(self, person: AlgorithmPerson, where: Union[None, int], position: int = None) -> None:
        super().add_person(person, where, position)
        person.current_affiliation = where

    def remove_person(self, person: AlgorithmPerson, where: Union[None, int]) -> bool:
        if super().remove_person(person, where):
            self.moved_elevator_people.add(person)
            person.current_affiliation = -1
            return True
        return False

    def rollback(self):
        for person in self.moved_elevator_people:
            if person.current_affiliation != -1:
                self.remove_person(person, person.current_affiliation)
            self.add_person(person, person.original_affiliation)

        self.moved_elevator_people.clear()
