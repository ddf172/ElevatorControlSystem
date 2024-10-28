from app.src.Managers.PeopleManager import PeopleManager
from app.src.Objects.Person import Person


class SystemPeopleManager(PeopleManager[Person]):
    def __init__(self):
        super().__init__()
