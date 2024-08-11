from Managers.PeopleManager import PeopleManager
from Objects.Person import Person


class SystemPeopleManager(PeopleManager[Person]):
    def __init__(self):
        super().__init__()
