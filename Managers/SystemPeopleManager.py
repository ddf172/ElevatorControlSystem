from Managers.PeopleManager import PeopleManager, T
from Objects.Person import Person


class SystemPeopleManager(PeopleManager[Person]):
    def __init__(self):
        super().__init__()

    def remove_person(self, person: Person, where: int) -> bool:
        if person.id in self.containers[where].floors[person.start_pos]:
            self.containers[where].floors[person.start_pos].pop(person.id)
            self.containers[where].count -= 1
            return True
        return False

    def move_person(self, person: Person, from_where: int, to_where: int) -> None:
        if not self.remove_person(person, from_where):
            raise IndexError("Person not found in the place")
        self.add_person(person, to_where)
