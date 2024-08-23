from Managers.PeopleManager import PeopleManager
from Objects.Person import AlgorithmPerson
from typing import Union


class EvaluatorPeopleManager(PeopleManager[AlgorithmPerson]):
    def __init__(self):
        super().__init__()
        self.moved_elevator_people = set()

    def add_person(self, person: AlgorithmPerson, where: Union[None, int], position: int = None) -> None:
        super().add_person(person, where, position)
        person.current_affiliation = where

    def remove_person(self, person: AlgorithmPerson, where: Union[None, int]) -> bool:
        if person.id in self.containers[where].floors[person.start_pos]:
            self.containers[where].floors[person.start_pos].pop(person.id)
            self.containers[where].count -= 1
            self.moved_elevator_people.add(person)

            # affiliation = -1 means that the person is not in any container
            person.current_affiliation = -1
            return True
        return False

    def move_person(self, person: AlgorithmPerson, from_where: Union[None, int], to_where: Union[None, int]) -> None:
        if not self.remove_person(person, from_where):
            raise IndexError("Person not found in the place")
        self.add_person(person, to_where)

    def rollback(self):
        for person in self.moved_elevator_people:
            if person.current_affiliation != -1:
                self.remove_person(person, person.current_affiliation)
            self.add_person(person, person.original_affiliation)

        self.moved_elevator_people.clear()
